# CarPool

Shared rides, car rental and car wash booking for Mumbai, with Razorpay payments and an admin dashboard.

A full rewrite of my 2022 semester project (plain PHP + MySQL). The original is kept in git history at the tag [`v1.0-legacy`](../../tree/v1.0-legacy).

![Home page](docs/screenshots/home.jpg)

## What it does

**Shared rides.** Drivers post a trip with the seats they can spare and a price per seat. Riders search by pickup, drop-off and date, book seats and pay online. The driver sees who's on board. Cancelling a booking gives the seats back, and cancelling a ride cancels every booking on it.

**Car rental.** Eight cars priced per kilometre. The full price with GST is shown before booking.

**Car wash.** Three plans at ten centres. Each centre has a fixed number of cars per time slot, so full and past slots can't be booked.

**Payments.** Razorpay Checkout in test or live mode. The server creates the order, checks the payment signature, and also listens to Razorpay's webhook, so a booking is confirmed even if the browser closes mid-payment. Without keys, a mock mode lets you click through the whole flow.

**Admin dashboard.** Revenue for the last 14 days and by service, every booking with filters (mark completed or cancel), payments with Razorpay IDs for refunds, ride moderation, users, and editing cars, wash plans and centres.

| Shared rides | Admin |
| --- | --- |
| ![Shared rides](docs/screenshots/shared-rides.jpg) | ![Admin overview](docs/screenshots/admin-overview.jpg) |
| ![Car wash](docs/screenshots/wash.jpg) | ![Rent a car](docs/screenshots/rent.jpg) |

## Tech stack

| Layer | Choice |
| --- | --- |
| Frontend | React 18, React Router, Vite, plain CSS |
| Backend | FastAPI, SQLAlchemy 2, Pydantic 2 |
| Database | PostgreSQL 16, Alembic migrations |
| Auth | bcrypt password hashes, JWT bearer tokens |
| Payments | Razorpay Orders API + Checkout, HMAC-SHA256 signature and webhook verification |
| Tests | pytest with FastAPI's TestClient |

## Run it locally

You need Python 3.11+, Node 18+ and Docker (or your own Postgres).

```bash
# 1. Database
docker compose up -d

# 2. API (http://localhost:8000, docs at /docs)
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
cp .env.example .env                                 # then set JWT_SECRET
alembic upgrade head
python -m app.seed --demo
uvicorn app.main:app --reload

# 3. Web app (http://localhost:5173), in a second terminal
cd frontend
npm install
npm run dev
```

Accounts created by the seed:

| Role | Email | Password |
| --- | --- | --- |
| Admin | admin@example.com | Admin@12345 |
| Demo driver | driver@example.com | Driver@12345 |

Change the admin password through `ADMIN_EMAIL` / `ADMIN_PASSWORD` in `.env` before deploying anywhere.

### Turn on Razorpay test payments

1. In the Razorpay dashboard, switch to Test Mode and generate API keys.
2. In `backend/.env`, set `PAYMENT_MODE=razorpay`, `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET`.
3. Optional: add a webhook pointing at `https://<your-api>/api/payments/webhook` for the `payment.captured` event, and put its secret in `RAZORPAY_WEBHOOK_SECRET`.
4. Pay with Razorpay's test cards or test UPI ID `success@razorpay`.

### Run the tests

```bash
cd backend
pytest                                   # SQLite, no setup needed
TEST_DATABASE_URL=postgresql+psycopg://carpool:carpool@localhost:5432/carpool_test pytest   # real Postgres
```

## How it's built

```
backend/
  app/
    main.py          app setup, CORS, routers
    models.py        tables (money stored as integer paise)
    schemas.py       request/response validation
    pricing.py       every price is calculated here
    bookings.py      shared rules: 15-minute holds, cancelling, seat release
    routers/         auth, rentals, wash, rides, payments, account, admin
    seed.py          cars, plans, centres, demo rides
  alembic/           migrations
  tests/
frontend/
  src/
    api.js           fetch wrapper with token and error handling
    pages/           Home, Carpool, OfferRide, Rent, Wash, MyBookings, admin/*
    components/      PayButton (Razorpay + mock), RouteLine, Status
docs/screenshots/
```

Decisions worth knowing:

- **The client never sends a price.** It sends what was chosen (car and km, plan and slot, ride and seats). The server works out the amount and stores it on the booking, and the payment order uses that stored amount.
- **Money is stored in paise** as integers, which is also what Razorpay uses, so there's no float rounding anywhere.
- **Unpaid bookings expire after 15 minutes.** They hold a ride seat or wash slot until then, so two people can't pay for the same last seat.
- **Seat booking locks the ride row** (`SELECT ... FOR UPDATE`) so simultaneous bookings can't oversell a ride.
- **Payment confirmation is idempotent**, so the browser callback and the webhook can both arrive without double-processing.
- **Catalogue items are hidden, never deleted**, because old bookings still point at them.
- Dates like "today", ride search days and wash slots use `TIMEZONE` (default `Asia/Kolkata`).

## What changed from v1

| v1 (2022, PHP) | v2 |
| --- | --- |
| SQL built from raw form input (injectable, login bypass) | ORM with bound parameters, validated input |
| Plain-text passwords | bcrypt hashes |
| Price calculated in jQuery and trusted by the server | Price calculated only on the server |
| Fake card form | Razorpay with signature and webhook verification |
| Rental insert didn't match the table, so bookings failed | Tested booking flows for all three services |
| No admin panel | Admin dashboard |
| Car rental + car wash | Plus shared rides |

## Ideas for later

Email or SMS confirmations, PDF invoices, ride ratings, map-based pickup points, automated refunds through the Razorpay Refunds API.
