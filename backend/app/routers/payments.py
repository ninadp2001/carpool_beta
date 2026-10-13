"""Razorpay payments.

Flow: the client asks for an order for one of its bookings, opens Razorpay Checkout
with that order, then sends the signed result back to /payments/verify. Razorpay also
calls /payments/webhook, so a booking still gets confirmed if the browser closes
before verify runs. With PAYMENT_MODE=mock the same flow works without keys.
"""
import hashlib
import hmac
import json
import secrets
from datetime import datetime, timezone

import httpx
from fastapi import APIRouter, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..bookings import get_booking, owner_id
from ..config import get_settings
from ..deps import DB, CurrentUser
from ..models import BookingStatus, Payment, PaymentStatus, RentalBooking, WashBooking
from ..schemas import MockPayIn, OrderIn, OrderOut, PaymentOut, VerifyIn

router = APIRouter(prefix="/payments", tags=["payments"])
RAZORPAY_ORDERS_URL = "https://api.razorpay.com/v1/orders"


def _describe(booking) -> str:
    if isinstance(booking, RentalBooking):
        return f"Car rental: {booking.car.name}, {booking.km} km"
    if isinstance(booking, WashBooking):
        return f"Car wash: {booking.plan.name}"
    return f"Carpool: {booking.ride.origin} to {booking.ride.destination}"


def _create_razorpay_order(amount: int, receipt: str) -> str:
    s = get_settings()
    if not (s.razorpay_key_id and s.razorpay_key_secret):
        raise HTTPException(503, "Payments aren't configured. Set the Razorpay keys in .env")
    try:
        r = httpx.post(
            RAZORPAY_ORDERS_URL,
            auth=(s.razorpay_key_id, s.razorpay_key_secret),
            json={"amount": amount, "currency": "INR", "receipt": receipt},
            timeout=15,
        )
        r.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(502, "Couldn't reach Razorpay. Try again in a minute.") from exc
    return r.json()["id"]


def _mark_paid(db: Session, payment: Payment, payment_id: str) -> None:
    """Idempotent: safe to call from both /verify and the webhook."""
    if payment.status == PaymentStatus.PAID:
        return
    payment.status = PaymentStatus.PAID
    payment.payment_id = payment_id
    payment.paid_at = datetime.now(timezone.utc)
    booking = get_booking(db, payment.booking_kind, payment.booking_id)
    if booking.status == BookingStatus.PENDING:
        booking.status = BookingStatus.CONFIRMED
    # If the hold expired and the booking was cancelled before the money arrived, the payment
    # is still recorded as paid so an admin can see it and refund it.
    db.commit()


@router.post("/order", response_model=OrderOut)
def create_order(body: OrderIn, user: CurrentUser, db: DB):
    s = get_settings()
    booking = get_booking(db, body.kind, body.booking_id)
    if owner_id(booking) != user.id:
        raise HTTPException(404, "Booking not found")
    if booking.status != BookingStatus.PENDING:
        raise HTTPException(409, "This booking doesn't need a payment")

    mode = "razorpay" if s.payment_mode == "razorpay" else "mock"
    receipt = f"{body.kind}-{booking.id}"
    order_id = (
        _create_razorpay_order(booking.total_amount, receipt)
        if mode == "razorpay"
        else f"order_mock_{secrets.token_hex(8)}"
    )
    db.add(
        Payment(
            user_id=user.id,
            booking_kind=body.kind,
            booking_id=booking.id,
            amount=booking.total_amount,
            provider=mode,
            order_id=order_id,
        )
    )
    db.commit()
    return OrderOut(
        mode=mode,
        order_id=order_id,
        amount=booking.total_amount,
        currency="INR",
        key_id=s.razorpay_key_id if mode == "razorpay" else None,
        description=_describe(booking),
        prefill={"name": user.full_name, "email": user.email, "contact": user.phone or ""},
    )


def _own_payment(db, order_id: str, user_id: int) -> Payment:
    payment = db.scalar(select(Payment).where(Payment.order_id == order_id))
    if payment is None or payment.user_id != user_id:
        raise HTTPException(404, "Payment not found")
    return payment


@router.post("/verify", response_model=PaymentOut)
def verify(body: VerifyIn, user: CurrentUser, db: DB):
    payment = _own_payment(db, body.razorpay_order_id, user.id)
    secret = get_settings().razorpay_key_secret.encode()
    expected = hmac.new(
        secret, f"{body.razorpay_order_id}|{body.razorpay_payment_id}".encode(), hashlib.sha256
    ).hexdigest()
    if not secret or not hmac.compare_digest(expected, body.razorpay_signature):
        payment.status = PaymentStatus.FAILED
        db.commit()
        raise HTTPException(400, "Payment couldn't be verified. If money left your account, contact support with your order ID.")
    _mark_paid(db, payment, body.razorpay_payment_id)
    return payment


@router.post("/mock/complete", response_model=PaymentOut)
def mock_complete(body: MockPayIn, user: CurrentUser, db: DB):
    if get_settings().payment_mode == "razorpay":
        raise HTTPException(404, "Not found")
    payment = _own_payment(db, body.order_id, user.id)
    _mark_paid(db, payment, f"pay_mock_{secrets.token_hex(8)}")
    return payment


@router.post("/webhook", include_in_schema=False)
async def webhook(request: Request, db: DB):
    secret = get_settings().razorpay_webhook_secret
    raw = await request.body()
    signature = request.headers.get("X-Razorpay-Signature", "")
    expected = hmac.new(secret.encode(), raw, hashlib.sha256).hexdigest()
    if not secret or not hmac.compare_digest(expected, signature):
        raise HTTPException(400, "Bad signature")
    event = json.loads(raw)
    if event.get("event") in ("payment.captured", "order.paid"):
        entity = event["payload"]["payment"]["entity"]
        payment = db.scalar(select(Payment).where(Payment.order_id == entity["order_id"]))
        if payment:
            _mark_paid(db, payment, entity["id"])
    return {"ok": True}
