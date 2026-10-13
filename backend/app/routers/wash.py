from datetime import date, datetime, time

from fastapi import APIRouter, HTTPException
from sqlalchemy import func, or_, select

from ..config import local_now
from ..bookings import hold_cutoff, release_expired_holds
from ..deps import DB, CurrentUser
from ..models import BookingStatus, WashBooking, WashCenter, WashPlan
from ..pricing import quote
from ..schemas import SlotOut, WashCenterOut, WashIn, WashOut, WashPlanOut

router = APIRouter(prefix="/wash", tags=["wash"])

SLOTS = [time(h) for h in (10, 12, 14, 16, 18)]


def _taken(db, center_id: int, day: date) -> dict[time, int]:
    """Bookings that occupy a slot: confirmed ones plus unpaid ones still on hold."""
    rows = db.execute(
        select(WashBooking.slot, func.count())
        .where(
            WashBooking.center_id == center_id,
            WashBooking.wash_date == day,
            or_(
                WashBooking.status == BookingStatus.CONFIRMED,
                (WashBooking.status == BookingStatus.PENDING)
                & (WashBooking.created_at >= hold_cutoff()),
            ),
        )
        .group_by(WashBooking.slot)
    ).all()
    return {slot: n for slot, n in rows}


@router.get("/plans", response_model=list[WashPlanOut])
def plans(db: DB):
    return db.scalars(select(WashPlan).where(WashPlan.is_active).order_by(WashPlan.price)).all()


@router.get("/centers", response_model=list[WashCenterOut])
def centers(db: DB):
    return db.scalars(select(WashCenter).where(WashCenter.is_active).order_by(WashCenter.area)).all()


@router.get("/centers/{center_id}/slots", response_model=list[SlotOut])
def slots(center_id: int, day: date, db: DB):
    center = db.get(WashCenter, center_id)
    if center is None or not center.is_active:
        raise HTTPException(404, "Wash center not found")
    taken = _taken(db, center_id, day)
    now = local_now()
    out = []
    for s in SLOTS:
        if day < now.date() or (day == now.date() and s <= now.time()):
            continue  # slot already passed
        out.append(SlotOut(slot=s, available=max(center.slot_capacity - taken.get(s, 0), 0)))
    return out


@router.post("/bookings", response_model=WashOut, status_code=201)
def book(body: WashIn, user: CurrentUser, db: DB):
    release_expired_holds(db)
    plan = db.get(WashPlan, body.plan_id)
    center = db.get(WashCenter, body.center_id)
    if plan is None or not plan.is_active or center is None or not center.is_active:
        raise HTTPException(404, "Pick an available plan and center")
    if body.slot not in SLOTS:
        raise HTTPException(422, "Pick one of the listed time slots")
    if datetime.combine(body.wash_date, body.slot) <= local_now():
        raise HTTPException(422, "That time slot has already passed")
    if _taken(db, center.id, body.wash_date).get(body.slot, 0) >= center.slot_capacity:
        raise HTTPException(409, "That slot just filled up. Pick another time.")
    q = quote(plan.price)
    booking = WashBooking(
        user_id=user.id,
        plan_id=plan.id,
        center_id=center.id,
        wash_date=body.wash_date,
        slot=body.slot,
        base_amount=q.base,
        tax_amount=q.tax,
        total_amount=q.total,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking
