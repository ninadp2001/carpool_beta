"""Load starting data. Safe to run more than once.

    python -m app.seed          # admin account, cars, wash plans and centers
    python -m app.seed --demo   # also a demo driver and a few upcoming carpool rides
"""
import sys
from datetime import datetime, time, timedelta, timezone

from sqlalchemy import select

from .config import get_settings
from .db import SessionLocal
from .models import Car, Ride, User, WashCenter, WashPlan
from .security import hash_password

CARS = [  # name, seats, rupees per km, image
    ("Maruti WagonR", 4, 8, "/cars/wagonr.jpg"),
    ("Tata Tiago", 4, 8, "/cars/tiago.jpg"),
    ("Maruti Swift Dzire", 5, 10, "/cars/dzire.jpg"),
    ("Hyundai Verna", 5, 10, "/cars/verna.jpg"),
    ("Maruti Ertiga", 7, 13, "/cars/ertiga.jpg"),
    ("Toyota Innova Crysta", 7, 13, "/cars/innova.jpg"),
    ("Tata Winger", 13, 18, "/cars/winger.jpg"),
    ("Force Tempo Traveller", 17, 22, "/cars/traveller.jpg"),
]

PLANS = [
    ("Basic", 550, ["Seat wash", "Vacuum", "Exterior wash"]),
    ("Premium", 750, ["Seat wash", "Vacuum", "Exterior wash", "Interior wet clean", "Window wipe"]),
    ("Complete", 1050, ["Seat wash", "Vacuum", "Exterior wash", "Interior wet clean", "Window wipe", "Disinfection", "Polish and detailing"]),
]

CENTERS = [
    ("Splash & Dash", "Kandivali West", "402 Blue Empress Apartments, Borsapada Road, opp. Poisar Gymkhana, Mumbai 400067", "7947411184"),
    ("PaajiAuto", "Malad West", "Evershine Nagar, New Link Road, near Movie Time Cinema, Mumbai 400064", "7949315450"),
    ("Extreme Car Care", "Ghansoli", "Shop 1, Vanai Niwas, Sector 2, near Ghansoli Station, Navi Mumbai 400701", "7947288767"),
    ("360 Moto Care", "Kharghar", "Shops B-15 and A-16, Shah Arcade, Sector 6, near Global IT Park, Navi Mumbai 410210", "7947179719"),
    ("Auto Launder", "Prabhadevi", "Plot 105B, S L Matkar Road, near Parel ST Depot, Mumbai 400025", "7947197114"),
    ("Baba Auto Garage", "Ghatkopar West", "Patan Wada Compound, LBS Marg, opp. Brand Factory, Mumbai 400084", "7947186715"),
    ("Zebro Auto Care", "Chembur East", "Plot 7, Laxmi Narayan Shopping Complex, Sion Trombay Road, Mumbai 400071", "7947168789"),
    ("VKS Auto Shine", "Thane West", "Next to Tata Motors, Eastern Express Highway, Thane 400602", "8045783832"),
    ("3C Crystal Clear Car", "Mulund West", "Zojawala Petroleum, LBS Marg, opp. Santoshi Mata Temple, Mumbai 400080", "7947371337"),
    ("Star Auto Care", "Colaba", "4th Pasta Lane, near Colaba Market Post Office, Mumbai 400005", "9920069887"),
]

DEMO_RIDES = [  # origin, destination, days ahead, hour, seats, rupees per seat, vehicle
    ("Andheri East", "Pune Hinjewadi", 1, 7, 3, 450, "Honda City, white"),
    ("Thane West", "BKC", 1, 8, 2, 150, "Maruti Baleno"),
    ("Borivali West", "Lower Parel", 2, 9, 3, 180, "Hyundai Creta"),
    ("Vashi", "Powai", 2, 18, 2, 120, "Tata Nexon EV"),
    ("Dadar", "Nashik", 4, 6, 4, 600, "Toyota Innova"),
]


def get_or_create(db, model, lookup: dict, **values):
    obj = db.scalar(select(model).filter_by(**lookup))
    if obj is None:
        obj = model(**lookup, **values)
        db.add(obj)
    return obj


def run(demo: bool = False) -> None:
    s = get_settings()
    with SessionLocal() as db:
        admin = get_or_create(
            db, User, {"email": s.admin_email.lower()},
            first_name="Admin", last_name="User", password_hash=hash_password(s.admin_password), is_admin=True,
        )
        admin.is_admin = True
        for name, seats, rate, image in CARS:
            get_or_create(db, Car, {"name": name}, seats=seats, rate_per_km=rate * 100, image=image)
        for name, price, features in PLANS:
            get_or_create(db, WashPlan, {"name": name}, price=price * 100, features=features)
        for name, area, address, phone in CENTERS:
            get_or_create(db, WashCenter, {"name": name}, area=area, address=address, phone=phone)

        if demo:
            driver = get_or_create(
                db, User, {"email": "driver@example.com"},
                first_name="Riya", last_name="Shah", phone="9800000000",
                password_hash=hash_password("Driver@12345"),
            )
            db.flush()
            ist = timezone(timedelta(hours=5, minutes=30))
            today = datetime.now(ist).date()
            for origin, dest, days, hour, seats, price, vehicle in DEMO_RIDES:
                depart = datetime.combine(today + timedelta(days=days), time(hour), tzinfo=ist)
                get_or_create(
                    db, Ride, {"driver_id": driver.id, "origin": origin, "destination": dest},
                    depart_at=depart, seats_total=seats, seats_available=seats,
                    price_per_seat=price * 100, vehicle=vehicle,
                )
        db.commit()
    print("Seed complete." + (" Demo driver: driver@example.com / Driver@12345" if demo else ""))


if __name__ == "__main__":
    run(demo="--demo" in sys.argv)
