from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .routers import account, admin, auth, payments, rentals, rides, wash

settings = get_settings()

app = FastAPI(
    title="CarPool API",
    version="2.0.0",
    description="Car rental, car wash booking and carpooling, with Razorpay payments.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for r in (auth, rentals, wash, rides, payments, account, admin):
    app.include_router(r.router, prefix="/api")


@app.get("/api/health", tags=["meta"])
def health():
    return {"ok": True, "payment_mode": settings.payment_mode}
