import { useEffect, useState } from "react";
import { api } from "../api";
import { useAuth } from "../auth";
import { addDaysISO, money, todayISO } from "../format";
import PayButton from "../components/PayButton";
import BookingDone from "../components/BookingDone";
import LoginToBook from "../components/LoginToBook";

export default function Rent() {
  const { user } = useAuth();
  const [cars, setCars] = useState(null);
  const [loadError, setLoadError] = useState("");
  const [car, setCar] = useState(null);
  const [form, setForm] = useState({ pickup_date: addDaysISO(1), km: 100 });
  const [quote, setQuote] = useState(null);
  const [booking, setBooking] = useState(null);
  const [paid, setPaid] = useState(false);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    api("/cars").then(setCars).catch((e) => setLoadError(e.message));
  }, []);

  // Ask the server for the price whenever the car or distance changes.
  useEffect(() => {
    setQuote(null);
    const km = Number(form.km);
    if (!car || !(km >= 10)) return;
    const t = setTimeout(() => {
      api("/rentals/quote", { method: "POST", body: { car_id: car.id, km } }).then(setQuote).catch(() => {});
    }, 250);
    return () => clearTimeout(t);
  }, [car, form.km]);

  function choose(c) {
    setCar(c);
    setBooking(null);
    setPaid(false);
    setError("");
    document.getElementById("rent-panel")?.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  async function book(e) {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      setBooking(await api("/rentals", { method: "POST", body: { car_id: car.id, km: Number(form.km), pickup_date: form.pickup_date } }));
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="page">
      <h1>Rent a car</h1>
      <p className="lede">Priced per kilometre. Choose a car, tell us how far you'll drive, and you'll see the total with 18% GST before you pay.</p>
      {loadError && <p className="form-error">{loadError}</p>}

      <div className="split">
        <ul className="car-grid" aria-label="Cars">
          {cars?.map((c) => (
            <li key={c.id}>
              <button
                className={`car-card${car?.id === c.id ? " selected" : ""}`}
                onClick={() => choose(c)}
                aria-pressed={car?.id === c.id}
              >
                <img src={c.image || "/cars/wagonr.jpg"} alt="" loading="lazy" width="800" height="600" />
                <span className="car-name">{c.name}</span>
                <span className="car-meta">
                  {c.seats} seats <strong>{money(c.rate_per_km)}/km</strong>
                </span>
              </button>
            </li>
          ))}
        </ul>

        <aside id="rent-panel" className="panel sticky">
          {!car && <p className="muted">Choose a car to see the price.</p>}
          {car && !booking && (
            <form onSubmit={book} className="stack">
              <h2>{car.name}</h2>
              <label className="field">
                <span>Pick-up date</span>
                <input type="date" required min={todayISO()} value={form.pickup_date} onChange={(e) => setForm({ ...form, pickup_date: e.target.value })} />
              </label>
              <label className="field">
                <span>Distance you'll drive (km)</span>
                <input type="number" required min={10} max={5000} value={form.km} onChange={(e) => setForm({ ...form, km: e.target.value })} />
              </label>
              <dl className="summary">
                <div><dt>{form.km || 0} km at {money(car.rate_per_km)}</dt><dd>{quote ? money(quote.base_amount) : "–"}</dd></div>
                <div><dt>GST</dt><dd>{quote ? money(quote.tax_amount) : "–"}</dd></div>
                <div className="total"><dt>Total</dt><dd>{quote ? money(quote.total_amount) : "–"}</dd></div>
              </dl>
              {error && <p className="form-error" role="alert">{error}</p>}
              {user ? (
                <button className="btn btn-primary" disabled={busy || !quote}>{busy ? "Booking…" : "Book this car"}</button>
              ) : (
                <LoginToBook />
              )}
            </form>
          )}
          {booking && !paid && (
            <div className="stack">
              <h2>{car.name}</h2>
              <p>Booked for {booking.pickup_date}, {booking.km} km. Pay within 15 minutes to confirm it.</p>
              <PayButton kind="rental" bookingId={booking.id} amount={booking.total_amount} onPaid={() => setPaid(true)} />
            </div>
          )}
          {paid && <BookingDone title="Your car is booked">{car.name} on {booking.pickup_date}. We'll have it ready.</BookingDone>}
        </aside>
      </div>
    </div>
  );
}
