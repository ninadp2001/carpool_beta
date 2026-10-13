import re
from datetime import date, datetime, time

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class ORM(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------- Auth


class RegisterIn(BaseModel):
    first_name: str = Field(min_length=2, max_length=60)
    last_name: str = Field(min_length=1, max_length=60)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=20)
    password: str = Field(min_length=8, max_length=128)

    @field_validator("first_name", "last_name")
    @classmethod
    def letters_only(cls, v: str) -> str:
        v = v.strip()
        if not re.fullmatch(r"[A-Za-z][A-Za-z .'-]*", v):
            raise ValueError("Use letters only")
        return v

    @field_validator("phone")
    @classmethod
    def phone_digits(cls, v: str | None) -> str | None:
        if v in (None, ""):
            return None
        digits = re.sub(r"[\s-]", "", v)
        if not re.fullmatch(r"\+?\d{10,13}", digits):
            raise ValueError("Enter a 10-digit mobile number")
        return digits

    @field_validator("password")
    @classmethod
    def strong_password(cls, v: str) -> str:
        if not (re.search(r"[a-z]", v) and re.search(r"[A-Z]", v) and re.search(r"\d", v)):
            raise ValueError("Password needs an uppercase letter, a lowercase letter and a number")
        return v


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class UserOut(ORM):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str | None
    is_admin: bool
    created_at: datetime


class PersonOut(ORM):
    """Shown only to the person themselves or to admins."""

    id: int
    first_name: str
    last_name: str
    email: str
    phone: str | None


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ---------------------------------------------------------------- Rental


class CarIn(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    seats: int = Field(ge=2, le=30)
    rate_per_km: int = Field(gt=0, description="Paise per km")
    image: str | None = None
    is_active: bool = True


class CarOut(ORM):
    id: int
    name: str
    seats: int
    rate_per_km: int
    image: str | None
    is_active: bool


class RentalQuoteIn(BaseModel):
    car_id: int
    km: int = Field(ge=10, le=5000)


class RentalIn(RentalQuoteIn):
    pickup_date: date


class QuoteOut(BaseModel):
    base_amount: int
    tax_amount: int
    total_amount: int


class RentalOut(ORM):
    id: int
    user: PersonOut
    car: CarOut
    pickup_date: date
    km: int
    rate_per_km: int
    base_amount: int
    tax_amount: int
    total_amount: int
    status: str
    created_at: datetime


# ---------------------------------------------------------------- Wash


class WashPlanIn(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    price: int = Field(gt=0)
    features: list[str] = []
    is_active: bool = True


class WashPlanOut(ORM):
    id: int
    name: str
    price: int
    features: list[str]
    is_active: bool


class WashCenterIn(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    area: str = Field(min_length=2, max_length=80)
    address: str
    phone: str | None = None
    slot_capacity: int = Field(default=2, ge=1, le=20)
    is_active: bool = True


class WashCenterOut(ORM):
    id: int
    name: str
    area: str
    address: str
    phone: str | None
    slot_capacity: int
    is_active: bool


class SlotOut(BaseModel):
    slot: time
    available: int


class WashIn(BaseModel):
    plan_id: int
    center_id: int
    wash_date: date
    slot: time


class WashOut(ORM):
    id: int
    user: PersonOut
    plan: WashPlanOut
    center: WashCenterOut
    wash_date: date
    slot: time
    base_amount: int
    tax_amount: int
    total_amount: int
    status: str
    created_at: datetime


# ---------------------------------------------------------------- Carpool


class DriverOut(ORM):
    id: int
    first_name: str
    last_name: str


class RideIn(BaseModel):
    origin: str = Field(min_length=2, max_length=120)
    destination: str = Field(min_length=2, max_length=120)
    depart_at: datetime
    seats_total: int = Field(ge=1, le=8)
    price_per_seat: int = Field(ge=0, le=500000, description="Paise")
    vehicle: str | None = Field(default=None, max_length=80)
    notes: str | None = Field(default=None, max_length=500)


class RideOut(ORM):
    id: int
    driver: DriverOut
    origin: str
    destination: str
    depart_at: datetime
    seats_total: int
    seats_available: int
    price_per_seat: int
    vehicle: str | None
    notes: str | None
    status: str


class RideBookingIn(BaseModel):
    seats: int = Field(ge=1, le=8)


class PassengerOut(ORM):
    id: int
    seats: int
    status: str
    passenger: DriverOut


class RideBookingOut(ORM):
    id: int
    passenger: PersonOut
    ride: RideOut
    seats: int
    base_amount: int
    tax_amount: int
    total_amount: int
    status: str
    created_at: datetime


class MyRideOut(RideOut):
    passengers: list[PassengerOut] = []


# ---------------------------------------------------------------- Payments


class OrderIn(BaseModel):
    kind: str = Field(pattern="^(rental|wash|ride)$")
    booking_id: int


class OrderOut(BaseModel):
    mode: str
    order_id: str
    amount: int
    currency: str
    key_id: str | None
    description: str
    prefill: dict


class VerifyIn(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str


class MockPayIn(BaseModel):
    order_id: str


class PaymentOut(ORM):
    id: int
    booking_kind: str
    booking_id: int
    amount: int
    provider: str
    order_id: str
    payment_id: str | None
    status: str
    created_at: datetime
    paid_at: datetime | None


# ---------------------------------------------------------------- Account


class MyBookingsOut(BaseModel):
    rentals: list[RentalOut]
    washes: list[WashOut]
    rides: list[RideBookingOut]
    offered: list[MyRideOut]
