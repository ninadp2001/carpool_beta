"""Database models.

All money is stored as integer paise (₹1 = 100 paise), which is also what Razorpay
expects, so there is never any float rounding between the database and the gateway.
"""
from datetime import date, datetime, time, timezone

from sqlalchemy import (
    JSON,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    Time,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class BookingStatus:
    PENDING = "pending_payment"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    ALL = (PENDING, CONFIRMED, CANCELLED, COMPLETED)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(60))
    last_name: Mapped[str] = mapped_column(String(60))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(20))
    password_hash: Mapped[str] = mapped_column(String(255))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


# ---------------------------------------------------------------- Rental


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80))
    seats: Mapped[int] = mapped_column(Integer)
    rate_per_km: Mapped[int] = mapped_column(Integer)  # paise per km
    image: Mapped[str | None] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class RentalBooking(Base):
    __tablename__ = "rental_bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"))
    pickup_date: Mapped[date] = mapped_column(Date)
    km: Mapped[int] = mapped_column(Integer)
    rate_per_km: Mapped[int] = mapped_column(Integer)  # snapshot at booking time
    base_amount: Mapped[int] = mapped_column(Integer)
    tax_amount: Mapped[int] = mapped_column(Integer)
    total_amount: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(20), default=BookingStatus.PENDING, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    user: Mapped[User] = relationship()
    car: Mapped[Car] = relationship()


# ---------------------------------------------------------------- Wash


class WashPlan(Base):
    __tablename__ = "wash_plans"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80))
    price: Mapped[int] = mapped_column(Integer)  # paise, before tax
    features: Mapped[list] = mapped_column(JSON, default=list)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class WashCenter(Base):
    __tablename__ = "wash_centers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    area: Mapped[str] = mapped_column(String(80))
    address: Mapped[str] = mapped_column(Text)
    phone: Mapped[str | None] = mapped_column(String(20))
    slot_capacity: Mapped[int] = mapped_column(Integer, default=2)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class WashBooking(Base):
    __tablename__ = "wash_bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    plan_id: Mapped[int] = mapped_column(ForeignKey("wash_plans.id"))
    center_id: Mapped[int] = mapped_column(ForeignKey("wash_centers.id"))
    wash_date: Mapped[date] = mapped_column(Date, index=True)
    slot: Mapped[time] = mapped_column(Time)
    base_amount: Mapped[int] = mapped_column(Integer)
    tax_amount: Mapped[int] = mapped_column(Integer)
    total_amount: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(20), default=BookingStatus.PENDING, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    user: Mapped[User] = relationship()
    plan: Mapped[WashPlan] = relationship()
    center: Mapped[WashCenter] = relationship()


# ---------------------------------------------------------------- Carpool


class RideStatus:
    OPEN = "open"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class Ride(Base):
    """A trip a driver offers, with seats other users can book."""

    __tablename__ = "rides"

    id: Mapped[int] = mapped_column(primary_key=True)
    driver_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    origin: Mapped[str] = mapped_column(String(120), index=True)
    destination: Mapped[str] = mapped_column(String(120), index=True)
    depart_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    seats_total: Mapped[int] = mapped_column(Integer)
    seats_available: Mapped[int] = mapped_column(Integer)
    price_per_seat: Mapped[int] = mapped_column(Integer)  # paise, before tax
    vehicle: Mapped[str | None] = mapped_column(String(80))
    notes: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default=RideStatus.OPEN, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    driver: Mapped[User] = relationship()
    bookings: Mapped[list["RideBooking"]] = relationship(back_populates="ride")


class RideBooking(Base):
    __tablename__ = "ride_bookings"
    __table_args__ = (UniqueConstraint("ride_id", "passenger_id", name="uq_ride_passenger"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    ride_id: Mapped[int] = mapped_column(ForeignKey("rides.id"), index=True)
    passenger_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    seats: Mapped[int] = mapped_column(Integer)
    base_amount: Mapped[int] = mapped_column(Integer)
    tax_amount: Mapped[int] = mapped_column(Integer)
    total_amount: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(20), default=BookingStatus.PENDING, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    ride: Mapped[Ride] = relationship(back_populates="bookings")
    passenger: Mapped[User] = relationship()


# ---------------------------------------------------------------- Payments


class PaymentStatus:
    CREATED = "created"
    PAID = "paid"
    FAILED = "failed"


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    booking_kind: Mapped[str] = mapped_column(String(10))  # rental | wash | ride
    booking_id: Mapped[int] = mapped_column(Integer)
    amount: Mapped[int] = mapped_column(Integer)  # paise
    currency: Mapped[str] = mapped_column(String(3), default="INR")
    provider: Mapped[str] = mapped_column(String(20))  # razorpay | mock
    order_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    payment_id: Mapped[str | None] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(10), default=PaymentStatus.CREATED, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    user: Mapped[User] = relationship()
