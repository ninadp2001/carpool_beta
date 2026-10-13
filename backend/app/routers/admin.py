from datetime import timedelta

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import func, select

from ..bookings import KINDS, cancel_booking, cancel_ride_and_bookings, get_booking
from ..config import local_now
from ..deps import DB, AdminUser
from ..models import (
    BookingStatus,
    Car,
    Payment,
    PaymentStatus,
    RentalBooking,
    Ride,
    RideBooking,
    RideStatus,
    User,
    WashBooking,
    WashCenter,
    WashPlan,
)
from ..schemas import (
    CarIn,
    CarOut,
    PaymentOut,
    RentalOut,
    RideBookingOut,
    RideOut,
    UserOut,
    WashCenterIn,
    WashCenterOut,
    WashOut,
    WashPlanIn,
    WashPlanOut,
)

router = APIRouter(prefix="/admin", tags=["admin"])


# ---------------------------------------------------------------- Dashboard


@router.get("/stats")
def stats(_: AdminUser, db: DB):
    paid = select(Payment).where(Payment.status == PaymentStatus.PAID).subquery()
    revenue_by_kind = dict(
        db.execute(select(paid.c.booking_kind, func.coalesce(func.sum(paid.c.amount), 0)).group_by(paid.c.booking_kind)).all()
    )
    since = local_now().date() - timedelta(days=13)
    day = func.date(Payment.paid_at)
    daily = db.execute(
        select(day, func.sum(Payment.amount))
        .where(Payment.status == PaymentStatus.PAID, Payment.paid_at >= since)
        .group_by(day)
        .order_by(day)
    ).all()

    def count(model, *where):
        return db.scalar(select(func.count()).select_from(model).where(*where)) or 0

    return {
        "users": count(User),
        "revenue_total": sum(revenue_by_kind.values()),
        "revenue_by_kind": {k: revenue_by_kind.get(k, 0) for k in ("rental", "wash", "ride")},
        "revenue_daily": [{"date": str(d), "amount": a} for d, a in daily],
        "confirmed": {
            "rental": count(RentalBooking, RentalBooking.status == BookingStatus.CONFIRMED),
            "wash": count(WashBooking, WashBooking.status == BookingStatus.CONFIRMED),
            "ride": count(RideBooking, RideBooking.status == BookingStatus.CONFIRMED),
        },
        "pending": sum(count(m, m.status == BookingStatus.PENDING) for m in KINDS.values()),
        "open_rides": count(Ride, Ride.status == RideStatus.OPEN),
    }


# ---------------------------------------------------------------- Bookings


@router.get("/bookings/rental", response_model=list[RentalOut])
def rental_bookings(_: AdminUser, db: DB, status: str | None = None):
    stmt = select(RentalBooking).order_by(RentalBooking.created_at.desc()).limit(200)
    return db.scalars(stmt.where(RentalBooking.status == status) if status else stmt).all()


@router.get("/bookings/wash", response_model=list[WashOut])
def wash_bookings(_: AdminUser, db: DB, status: str | None = None):
    stmt = select(WashBooking).order_by(WashBooking.created_at.desc()).limit(200)
    return db.scalars(stmt.where(WashBooking.status == status) if status else stmt).all()


@router.get("/bookings/ride", response_model=list[RideBookingOut])
def ride_bookings(_: AdminUser, db: DB, status: str | None = None):
    stmt = select(RideBooking).order_by(RideBooking.created_at.desc()).limit(200)
    return db.scalars(stmt.where(RideBooking.status == status) if status else stmt).all()


class StatusIn(BaseModel):
    status: str


@router.patch("/bookings/{kind}/{booking_id}")
def set_booking_status(kind: str, booking_id: int, body: StatusIn, _: AdminUser, db: DB):
    booking = get_booking(db, kind, booking_id)
    if body.status == BookingStatus.CANCELLED:
        cancel_booking(db, booking)
    elif body.status == BookingStatus.COMPLETED:
        if booking.status != BookingStatus.CONFIRMED:
            raise HTTPException(409, "Only confirmed bookings can be marked completed")
        booking.status = BookingStatus.COMPLETED
    else:
        raise HTTPException(422, "Status can be set to cancelled or completed")
    db.commit()
    return {"status": booking.status}


# ---------------------------------------------------------------- Catalogue CRUD


def _crud(model, schema_in, schema_out, path: str, order_by):
    @router.get(f"/{path}", response_model=list[schema_out], name=f"list_{path}")
    def list_items(_: AdminUser, db: DB):
        return db.scalars(select(model).order_by(order_by)).all()

    @router.post(f"/{path}", response_model=schema_out, status_code=201, name=f"create_{path}")
    def create(body: schema_in, _: AdminUser, db: DB):  # type: ignore[valid-type]
        item = model(**body.model_dump())
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @router.put(f"/{path}/{{item_id}}", response_model=schema_out, name=f"update_{path}")
    def update(item_id: int, body: schema_in, _: AdminUser, db: DB):  # type: ignore[valid-type]
        item = db.get(model, item_id)
        if item is None:
            raise HTTPException(404, "Not found")
        for k, v in body.model_dump().items():
            setattr(item, k, v)
        db.commit()
        return item


# No DELETE on purpose: old bookings point at these rows. Set is_active=false to hide one.
_crud(Car, CarIn, CarOut, "cars", Car.seats)
_crud(WashPlan, WashPlanIn, WashPlanOut, "plans", WashPlan.price)
_crud(WashCenter, WashCenterIn, WashCenterOut, "centers", WashCenter.area)


# ---------------------------------------------------------------- Users, rides, payments


@router.get("/users", response_model=list[UserOut])
def users(_: AdminUser, db: DB, q: str | None = Query(None, max_length=100)):
    stmt = select(User).order_by(User.created_at.desc()).limit(200)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(User.email.ilike(like) | User.first_name.ilike(like) | User.last_name.ilike(like))
    return db.scalars(stmt).all()


@router.get("/rides", response_model=list[RideOut])
def rides(_: AdminUser, db: DB):
    return db.scalars(select(Ride).order_by(Ride.depart_at.desc()).limit(200)).all()


@router.post("/rides/{ride_id}/cancel", response_model=RideOut)
def cancel_ride(ride_id: int, _: AdminUser, db: DB):
    ride = db.get(Ride, ride_id)
    if ride is None:
        raise HTTPException(404, "Ride not found")
    cancel_ride_and_bookings(ride)
    db.commit()
    return ride


@router.get("/payments", response_model=list[PaymentOut])
def payments(_: AdminUser, db: DB):
    return db.scalars(select(Payment).order_by(Payment.created_at.desc()).limit(200)).all()
