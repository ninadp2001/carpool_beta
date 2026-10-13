"""End-to-end API tests.

Runs against TEST_DATABASE_URL (a throwaway Postgres DB) if set, otherwise SQLite in a temp file.
"""
import hashlib
import hmac
import os
import tempfile
from datetime import date, datetime, timedelta, timezone

_tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
os.environ["DATABASE_URL"] = os.environ.get("TEST_DATABASE_URL", f"sqlite:///{_tmp.name}")
os.environ["PAYMENT_MODE"] = "mock"
os.environ["JWT_SECRET"] = "test-secret"
os.environ["RAZORPAY_KEY_SECRET"] = "rzp_secret"
os.environ["RAZORPAY_WEBHOOK_SECRET"] = "hook_secret"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app import models  # noqa: E402,F401
from app.db import Base, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.seed import run as seed  # noqa: E402

client = TestClient(app)
TOMORROW = date.today() + timedelta(days=1)


@pytest.fixture(autouse=True, scope="module")
def database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    seed()
    yield
    Base.metadata.drop_all(engine)


def signup(email: str) -> dict:
    r = client.post("/api/auth/register", json={
        "first_name": "Test", "last_name": "User", "email": email, "password": "Secret123",
    })
    assert r.status_code == 201, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def admin_headers() -> dict:
    r = client.post("/api/auth/login", json={"email": "admin@example.com", "password": "Admin@12345"})
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def pay(headers, kind, booking_id):
    order = client.post("/api/payments/order", json={"kind": kind, "booking_id": booking_id}, headers=headers)
    assert order.status_code == 200, order.text
    r = client.post("/api/payments/mock/complete", json={"order_id": order.json()["order_id"]}, headers=headers)
    assert r.json()["status"] == "paid"
    return order.json()


def test_auth_rules():
    h = signup("a@example.com")
    assert client.get("/api/auth/me", headers=h).json()["email"] == "a@example.com"
    # duplicate email, case-insensitive
    r = client.post("/api/auth/register", json={
        "first_name": "X", "last_name": "Y", "email": "A@example.com", "password": "Secret123"})
    assert r.status_code in (409, 422)
    assert client.post("/api/auth/register", json={
        "first_name": "Weak", "last_name": "Pw", "email": "w@example.com", "password": "password"}).status_code == 422
    assert client.post("/api/auth/login", json={"email": "a@example.com", "password": "nope"}).status_code == 401
    # the classic legacy injection no longer works
    assert client.post("/api/auth/login", json={"email": "a@example.com", "password": "' OR '1'='1"}).status_code == 401
    assert client.get("/api/me/bookings").status_code == 401


def test_rental_price_is_server_side_and_payment_confirms():
    h = signup("rent@example.com")
    car = client.get("/api/cars").json()[0]
    q = client.post("/api/rentals/quote", json={"car_id": car["id"], "km": 100}).json()
    assert q["base_amount"] == car["rate_per_km"] * 100
    assert q["total_amount"] == q["base_amount"] + round(q["base_amount"] * 0.18)

    # extra "total_amount" field from a tampering client is ignored
    r = client.post("/api/rentals", json={
        "car_id": car["id"], "km": 100, "pickup_date": str(TOMORROW), "total_amount": 1}, headers=h)
    assert r.status_code == 201 and r.json()["total_amount"] == q["total_amount"]
    rental = r.json()
    assert rental["status"] == "pending_payment"

    order = pay(h, "rental", rental["id"])
    assert order["amount"] == q["total_amount"]
    mine = client.get("/api/me/bookings", headers=h).json()
    assert mine["rentals"][0]["status"] == "confirmed"
    # can't pay twice
    assert client.post("/api/payments/order", json={"kind": "rental", "booking_id": rental["id"]}, headers=h).status_code == 409


def test_cannot_touch_someone_elses_booking():
    owner, other = signup("owner@example.com"), signup("other@example.com")
    car = client.get("/api/cars").json()[0]
    b = client.post("/api/rentals", json={"car_id": car["id"], "km": 50, "pickup_date": str(TOMORROW)}, headers=owner).json()
    assert client.post("/api/payments/order", json={"kind": "rental", "booking_id": b["id"]}, headers=other).status_code == 404
    assert client.post(f"/api/me/bookings/rental/{b['id']}/cancel", headers=other).status_code == 404


def test_wash_slot_capacity():
    plan = client.get("/api/wash/plans").json()[0]
    center = client.get("/api/wash/centers").json()[0]
    slots = client.get(f"/api/wash/centers/{center['id']}/slots", params={"day": str(TOMORROW)}).json()
    assert len(slots) == 5 and slots[0]["available"] == center["slot_capacity"]
    body = {"plan_id": plan["id"], "center_id": center["id"], "wash_date": str(TOMORROW), "slot": "10:00:00"}
    for i in range(center["slot_capacity"]):
        assert client.post("/api/wash/bookings", json=body, headers=signup(f"wash{i}@example.com")).status_code == 201
    assert client.post("/api/wash/bookings", json=body, headers=signup("late@example.com")).status_code == 409
    assert client.post("/api/wash/bookings", json={**body, "slot": "11:00:00"}, headers=signup("odd@example.com")).status_code == 422


def test_carpool_offer_book_cancel():
    driver, rider = signup("driver1@example.com"), signup("rider@example.com")
    depart = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
    ride = client.post("/api/rides", json={
        "origin": "Andheri", "destination": "Pune", "depart_at": depart,
        "seats_total": 3, "price_per_seat": 40000}, headers=driver).json()

    found = client.get("/api/rides", params={"origin": "andheri", "destination": "pun"}).json()
    assert any(r["id"] == ride["id"] for r in found)

    assert client.post(f"/api/rides/{ride['id']}/book", json={"seats": 1}, headers=driver).status_code == 422
    assert client.post(f"/api/rides/{ride['id']}/book", json={"seats": 4}, headers=rider).status_code == 409
    b = client.post(f"/api/rides/{ride['id']}/book", json={"seats": 2}, headers=rider).json()
    assert b["total_amount"] == 80000 + round(80000 * 0.18)
    assert client.get(f"/api/rides/{ride['id']}").json()["seats_available"] == 1
    assert client.post(f"/api/rides/{ride['id']}/book", json={"seats": 1}, headers=rider).status_code == 409

    # cancelling gives the seats back, and the rider can book again
    assert client.post(f"/api/me/bookings/ride/{b['id']}/cancel", headers=rider).json()["status"] == "cancelled"
    assert client.get(f"/api/rides/{ride['id']}").json()["seats_available"] == 3
    again = client.post(f"/api/rides/{ride['id']}/book", json={"seats": 1}, headers=rider)
    assert again.status_code == 201
    pay(rider, "ride", again.json()["id"])

    offered = client.get("/api/me/bookings", headers=driver).json()["offered"]
    assert offered[0]["passengers"][0]["status"] == "confirmed"

    # driver cancels the whole ride
    client.post(f"/api/rides/{ride['id']}/cancel", headers=driver)
    assert client.get("/api/me/bookings", headers=rider).json()["rides"][0]["status"] == "cancelled"


def test_razorpay_signature_verification():
    h = signup("sig@example.com")
    car = client.get("/api/cars").json()[0]
    b = client.post("/api/rentals", json={"car_id": car["id"], "km": 20, "pickup_date": str(TOMORROW)}, headers=h).json()
    order_id = client.post("/api/payments/order", json={"kind": "rental", "booking_id": b["id"]}, headers=h).json()["order_id"]
    bad = client.post("/api/payments/verify", json={
        "razorpay_order_id": order_id, "razorpay_payment_id": "pay_x", "razorpay_signature": "forged"}, headers=h)
    assert bad.status_code == 400
    sig = hmac.new(b"rzp_secret", f"{order_id}|pay_x".encode(), hashlib.sha256).hexdigest()
    ok = client.post("/api/payments/verify", json={
        "razorpay_order_id": order_id, "razorpay_payment_id": "pay_x", "razorpay_signature": sig}, headers=h)
    assert ok.status_code == 200 and ok.json()["status"] == "paid"


def test_admin():
    user = signup("plain@example.com")
    assert client.get("/api/admin/stats", headers=user).status_code == 403
    a = admin_headers()
    stats = client.get("/api/admin/stats", headers=a).json()
    assert stats["revenue_total"] > 0 and stats["confirmed"]["rental"] >= 1
    car = client.post("/api/admin/cars", json={"name": "Test EV", "seats": 5, "rate_per_km": 1200}, headers=a).json()
    client.put(f"/api/admin/cars/{car['id']}", json={**car, "is_active": False}, headers=a)
    assert all(c["id"] != car["id"] for c in client.get("/api/cars").json())
    rentals = client.get("/api/admin/bookings/rental", params={"status": "confirmed"}, headers=a).json()
    r = client.patch(f"/api/admin/bookings/rental/{rentals[0]['id']}", json={"status": "completed"}, headers=a)
    assert r.json()["status"] == "completed"
