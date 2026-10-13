from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from ..config import local_now
from ..deps import DB, CurrentUser
from ..models import Car, RentalBooking
from ..pricing import quote
from ..schemas import CarOut, QuoteOut, RentalIn, RentalOut, RentalQuoteIn

router = APIRouter(tags=["rentals"])


def _active_car(db, car_id: int) -> Car:
    car = db.get(Car, car_id)
    if car is None or not car.is_active:
        raise HTTPException(404, "This car isn't available")
    return car


@router.get("/cars", response_model=list[CarOut])
def list_cars(db: DB):
    return db.scalars(select(Car).where(Car.is_active).order_by(Car.seats, Car.rate_per_km)).all()


@router.post("/rentals/quote", response_model=QuoteOut)
def rental_quote(body: RentalQuoteIn, db: DB):
    car = _active_car(db, body.car_id)
    q = quote(car.rate_per_km * body.km)
    return QuoteOut(base_amount=q.base, tax_amount=q.tax, total_amount=q.total)


@router.post("/rentals", response_model=RentalOut, status_code=201)
def create_rental(body: RentalIn, user: CurrentUser, db: DB):
    if body.pickup_date < local_now().date():
        raise HTTPException(422, "Pick a date from today onwards")
    car = _active_car(db, body.car_id)
    q = quote(car.rate_per_km * body.km)
    booking = RentalBooking(
        user_id=user.id,
        car_id=car.id,
        pickup_date=body.pickup_date,
        km=body.km,
        rate_per_km=car.rate_per_km,
        base_amount=q.base,
        tax_amount=q.tax,
        total_amount=q.total,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking
