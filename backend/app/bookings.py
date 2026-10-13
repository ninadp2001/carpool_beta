"""Shared booking rules used by the booking routers, payments and admin."""
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import BookingStatus, RentalBooking, Ride, RideBooking, RideStatus, WashBooking

KINDS = {"rental": RentalBooking, "wash": WashBooking, "ride": RideBooking}

# An unpaid booking holds its seat or wash slot for this long, then is released.
HOLD_MINUTES = 15


def hold_cutoff() -> datetime:
    return datetime.now(timezone.utc) - timedelta(minutes=HOLD_MINUTES)


def owner_id(booking) -> int:
    return booking.passenger_id if isinstance(booking, RideBooking) else booking.user_id


def get_booking(db: Session, kind: str, booking_id: int):
    model = KINDS.get(kind)
    booking = db.get(model, booking_id) if model else None
    if booking is None:
        raise HTTPException(404, "Booking not found")
    return booking


def cancel_booking(db: Session, booking) -> None:
    """Cancel a booking and give any held ride seats back."""
    if booking.status in (BookingStatus.CANCELLED, BookingStatus.COMPLETED):
        raise HTTPException(409, f"This booking is already {booking.status}")
    if isinstance(booking, RideBooking):
        booking.ride.seats_available += booking.seats
    booking.status = BookingStatus.CANCELLED


def release_expired_holds(db: Session) -> None:
    """Cancel unpaid bookings older than the hold window so seats and slots free up."""
    cutoff = hold_cutoff()
    for model in (RideBooking, WashBooking, RentalBooking):
        stale = db.scalars(
            select(model).where(model.status == BookingStatus.PENDING, model.created_at < cutoff)
        ).all()
        for b in stale:
            cancel_booking(db, b)
    db.commit()


def cancel_ride_and_bookings(ride: Ride) -> None:
    """Cancel an offered ride and every booking on it."""
    if ride.status != RideStatus.OPEN:
        raise HTTPException(409, f"This ride is already {ride.status}")
    ride.status = RideStatus.CANCELLED
    for b in ride.bookings:
        if b.status in (BookingStatus.PENDING, BookingStatus.CONFIRMED):
            b.status = BookingStatus.CANCELLED
