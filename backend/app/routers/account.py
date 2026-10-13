from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from ..bookings import cancel_booking, get_booking, owner_id, release_expired_holds
from ..deps import DB, CurrentUser
from ..models import RentalBooking, Ride, RideBooking, WashBooking
from ..schemas import MyBookingsOut

router = APIRouter(prefix="/me", tags=["account"])


@router.get("/bookings", response_model=MyBookingsOut)
def my_bookings(user: CurrentUser, db: DB):
    release_expired_holds(db)
    newest = lambda m: m.created_at.desc()  # noqa: E731
    return MyBookingsOut(
        rentals=db.scalars(select(RentalBooking).where(RentalBooking.user_id == user.id).order_by(newest(RentalBooking))).all(),
        washes=db.scalars(select(WashBooking).where(WashBooking.user_id == user.id).order_by(newest(WashBooking))).all(),
        rides=db.scalars(select(RideBooking).where(RideBooking.passenger_id == user.id).order_by(newest(RideBooking))).all(),
        offered=[
            {**_ride_dict(r), "passengers": [b for b in r.bookings if b.status != "cancelled"]}
            for r in db.scalars(select(Ride).where(Ride.driver_id == user.id).order_by(Ride.depart_at.desc())).all()
        ],
    )


def _ride_dict(ride: Ride) -> dict:
    return {c: getattr(ride, c) for c in (
        "id", "driver", "origin", "destination", "depart_at", "seats_total",
        "seats_available", "price_per_seat", "vehicle", "notes", "status",
    )}


@router.post("/bookings/{kind}/{booking_id}/cancel")
def cancel(kind: str, booking_id: int, user: CurrentUser, db: DB):
    booking = get_booking(db, kind, booking_id)
    if owner_id(booking) != user.id:
        raise HTTPException(404, "Booking not found")
    cancel_booking(db, booking)
    db.commit()
    return {"status": booking.status}
