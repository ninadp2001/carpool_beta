from datetime import date, datetime, time, timedelta, timezone

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select

from ..config import local_tz
from ..bookings import cancel_ride_and_bookings, release_expired_holds
from ..deps import DB, CurrentUser
from ..models import BookingStatus, Ride, RideBooking, RideStatus
from ..pricing import quote
from ..schemas import RideBookingIn, RideBookingOut, RideIn, RideOut

router = APIRouter(prefix="/rides", tags=["carpool"])


def _as_utc(dt: datetime) -> datetime:
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


@router.get("", response_model=list[RideOut])
def search(
    db: DB,
    origin: str | None = Query(None, max_length=120),
    destination: str | None = Query(None, max_length=120),
    day: date | None = None,
    seats: int = Query(1, ge=1, le=8),
):
    release_expired_holds(db)
    stmt = select(Ride).where(
        Ride.status == RideStatus.OPEN,
        Ride.seats_available >= seats,
        Ride.depart_at > datetime.now(timezone.utc),
    )
    if origin:
        stmt = stmt.where(Ride.origin.ilike(f"%{origin.strip()}%"))
    if destination:
        stmt = stmt.where(Ride.destination.ilike(f"%{destination.strip()}%"))
    if day:
        start = datetime.combine(day, time.min, tzinfo=local_tz())
        stmt = stmt.where(Ride.depart_at >= start, Ride.depart_at < start + timedelta(days=1))
    return db.scalars(stmt.order_by(Ride.depart_at).limit(100)).all()


@router.get("/{ride_id}", response_model=RideOut)
def get_ride(ride_id: int, db: DB):
    ride = db.get(Ride, ride_id)
    if ride is None:
        raise HTTPException(404, "Ride not found")
    return ride


@router.post("", response_model=RideOut, status_code=201)
def offer_ride(body: RideIn, user: CurrentUser, db: DB):
    depart_at = _as_utc(body.depart_at)
    if depart_at <= datetime.now(timezone.utc) + timedelta(minutes=30):
        raise HTTPException(422, "Departure must be at least 30 minutes from now")
    if body.origin.strip().lower() == body.destination.strip().lower():
        raise HTTPException(422, "Pickup and drop-off must be different")
    ride = Ride(
        driver_id=user.id,
        origin=body.origin.strip(),
        destination=body.destination.strip(),
        depart_at=depart_at,
        seats_total=body.seats_total,
        seats_available=body.seats_total,
        price_per_seat=body.price_per_seat,
        vehicle=body.vehicle,
        notes=body.notes,
    )
    db.add(ride)
    db.commit()
    db.refresh(ride)
    return ride


@router.post("/{ride_id}/cancel", response_model=RideOut)
def cancel_ride(ride_id: int, user: CurrentUser, db: DB):
    ride = db.get(Ride, ride_id)
    if ride is None or ride.driver_id != user.id:
        raise HTTPException(404, "Ride not found")
    cancel_ride_and_bookings(ride)
    db.commit()
    return ride


@router.post("/{ride_id}/book", response_model=RideBookingOut, status_code=201)
def book_seats(ride_id: int, body: RideBookingIn, user: CurrentUser, db: DB):
    release_expired_holds(db)
    # Lock the ride row so two people can't grab the last seat at the same time (Postgres).
    ride = db.scalar(select(Ride).where(Ride.id == ride_id).with_for_update())
    if ride is None or ride.status != RideStatus.OPEN:
        raise HTTPException(404, "This ride isn't open for booking")
    if ride.driver_id == user.id:
        raise HTTPException(422, "You can't book a seat on your own ride")
    if _as_utc(ride.depart_at) <= datetime.now(timezone.utc):
        raise HTTPException(422, "This ride has already left")
    if body.seats > ride.seats_available:
        raise HTTPException(409, f"Only {ride.seats_available} seat(s) left")

    existing = db.scalar(
        select(RideBooking).where(RideBooking.ride_id == ride.id, RideBooking.passenger_id == user.id)
    )
    if existing and existing.status in (BookingStatus.PENDING, BookingStatus.CONFIRMED):
        raise HTTPException(409, "You already have a booking on this ride")

    q = quote(ride.price_per_seat * body.seats)
    if existing:  # re-booking after a cancellation reuses the row (one row per passenger per ride)
        booking = existing
        booking.seats, booking.status = body.seats, BookingStatus.PENDING
        booking.base_amount, booking.tax_amount, booking.total_amount = q.base, q.tax, q.total
        booking.created_at = datetime.now(timezone.utc)
    else:
        booking = RideBooking(
            ride_id=ride.id,
            passenger_id=user.id,
            seats=body.seats,
            base_amount=q.base,
            tax_amount=q.tax,
            total_amount=q.total,
        )
        db.add(booking)
    if q.total == 0:  # free rides don't need a payment step
        booking.status = BookingStatus.CONFIRMED
    ride.seats_available -= body.seats
    db.commit()
    db.refresh(booking)
    return booking
