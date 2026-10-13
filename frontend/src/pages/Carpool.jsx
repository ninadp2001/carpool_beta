import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { api } from "../api";
import { useAuth } from "../auth";
import { clock, day, money, todayISO } from "../format";
import RouteLine from "../components/Route";
import PayButton from "../components/PayButton";
import BookingDone from "../components/BookingDone";
import LoginToBook from "../components/LoginToBook";

function RidePanel({ rideId, onChanged }) {
  const { user } = useAuth();
  const [ride, setRide] = useState(null);
  const [seats, setSeats] = useState(1);
  const [booking, setBooking] = useState(null);
  const [paid, setPaid] = useState(false);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    setRide(null);
    setBooking(null);
    setPaid(false);
    setError("");
    setSeats(1);
    api(`/rides/${rideId}`).then(setRide).catch((e) => setError(e.message));
  }, [rideId]);

  async function book() {
    setBusy(true);
    setError("");
    try {
      const b = await api(`/rides/${rideId}/book`, { method: "POST", body: { seats } });
      setBooking(b);
      if (b.status === "confirmed") setPaid(true); // free ride
      onChanged();
    } catch (e) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  }

  if (!ride) return <aside className="panel">{error ? <p className="form-error">{error}</p> : <p className="muted">Loading…</p>}</aside>;
  const own = user?.id === ride.driver.id;

  return (
    <aside className="panel sticky ride-panel">
      <p className="muted">{day(ride.depart_at)}, leaves at {clock(ride.depart_at)}</p>
      <RouteLine from={ride.origin} to={ride.destination} size="lg" />
      <dl className="summary">
        <div><dt>Driver</dt><dd>{ride.driver.first_name} {ride.driver.last_name[0]}.</dd></div>
        {ride.vehicle && <div><dt>Car</dt><dd>{ride.vehicle}</dd></div>}
        <div><dt>Seats left</dt><dd>{ride.seats_available} of {ride.seats_total}</dd></div>
        <div><dt>Per seat</dt><dd>{money(ride.price_per_seat)} + GST</dd></div>
      </dl>
      {ride.notes && <p className="notes">{ride.notes}</p>}

      {error && <p className="form-error" role="alert">{error}</p>}
      {!user && <LoginToBook />}
      {own && <p className="muted">This is your ride. Manage it from <Link to="/bookings">My bookings</Link>.</p>}
      {user && !own && !booking && ride.seats_available > 0 && (
        <div className="row-gap align-end">
          <label className="field seats-field">
            <span>Seats</span>
            <select value={seats} onChange={(e) => setSeats(Number(e.target.value))}>
              {Array.from({ length: ride.seats_available }, (_, i) => i + 1).map((n) => <option key={n}>{n}</option>)}
            </select>
          </label>
          <button className="btn btn-primary" onClick={book} disabled={busy}>
            {busy ? "Holding seats…" : `Book ${seats} seat${seats > 1 ? "s" : ""}`}
          </button>
        </div>
      )}
      {booking && !paid && (
        <div className="stack">
          <p>{booking.seats} seat{booking.seats > 1 ? "s" : ""} held for 15 minutes.</p>
          <PayButton kind="ride" bookingId={booking.id} amount={booking.total_amount} onPaid={() => setPaid(true)} />
        </div>
      )}
      {paid && <BookingDone title="You're on the ride">Be at {ride.origin} by {clock(ride.depart_at)} on {day(ride.depart_at)}.</BookingDone>}
    </aside>
  );
}

export default function Carpool() {
  const [params, setParams] = useSearchParams();
  const [form, setForm] = useState({
    origin: params.get("origin") ?? "",
    destination: params.get("destination") ?? "",
    day: params.get("day") ?? "",
    seats: params.get("seats") ?? "1",
  });
  const [rides, setRides] = useState(null);
  const [error, setError] = useState("");
  const selected = params.get("ride");

  const query = ["origin", "destination", "day", "seats"].map((k) => params.get(k) ?? "").join("|");
  const load = () =>
    api("/rides", {
      params: { origin: params.get("origin"), destination: params.get("destination"), day: params.get("day"), seats: params.get("seats") },
    })
      .then(setRides)
      .catch((e) => setError(e.message));

  useEffect(() => {
    load();
  }, [query]); // eslint-disable-line react-hooks/exhaustive-deps

  function search(e) {
    e.preventDefault();
    const next = Object.fromEntries(Object.entries(form).filter(([, v]) => v && v !== "1"));
    setParams(next);
  }

  function select(id) {
    const next = new URLSearchParams(params);
    next.set("ride", id);
    setParams(next, { replace: true });
    // On narrow screens the details panel sits below the list.
    requestAnimationFrame(() => document.querySelector(".ride-panel")?.scrollIntoView({ behavior: "smooth", block: "start" }));
  }

  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });
  return (
    <div className="page">
      <div className="title-row">
        <h1>Shared rides</h1>
        <Link to="/carpool/offer" className="btn btn-outline">Offer a ride</Link>
      </div>

      <form className="search-bar" onSubmit={search} role="search">
        <label className="field"><span>From</span><input placeholder="e.g. Andheri" value={form.origin} onChange={set("origin")} /></label>
        <label className="field"><span>To</span><input placeholder="e.g. Pune" value={form.destination} onChange={set("destination")} /></label>
        <label className="field"><span>Date</span><input type="date" min={todayISO()} value={form.day} onChange={set("day")} /></label>
        <label className="field narrow-field">
          <span>Seats</span>
          <select value={form.seats} onChange={set("seats")}>{[1, 2, 3, 4].map((n) => <option key={n}>{n}</option>)}</select>
        </label>
        <button className="btn btn-primary">Search</button>
      </form>

      {error && <p className="form-error">{error}</p>}
      <div className="split">
        <div>
          {rides === null && <p className="muted">Loading rides…</p>}
          {rides?.length === 0 && (
            <div className="empty">
              <p>No rides match that search yet.</p>
              <p className="muted">Try a nearby area or another date, or <Link to="/carpool/offer">offer this ride yourself</Link>.</p>
            </div>
          )}
          <ul className="ride-list">
            {rides?.map((r) => (
              <li key={r.id}>
                <button className={`ride-row${String(r.id) === selected ? " selected" : ""}`} onClick={() => select(r.id)} aria-pressed={String(r.id) === selected}>
                  <span className="departure-time"><strong>{clock(r.depart_at)}</strong>{day(r.depart_at)}</span>
                  <RouteLine from={r.origin} to={r.destination} />
                  <span className="departure-meta">{money(r.price_per_seat)}<small>{r.seats_available} seat{r.seats_available > 1 ? "s" : ""} left</small></span>
                </button>
              </li>
            ))}
          </ul>
        </div>
        {selected ? <RidePanel rideId={selected} onChanged={load} /> : <aside className="panel placeholder"><p className="muted">Choose a ride to see the details and book a seat.</p></aside>}
      </div>
    </div>
  );
}
