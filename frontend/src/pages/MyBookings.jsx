import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";
import { clock, day, money, slotLabel } from "../format";
import PayButton from "../components/PayButton";
import RouteLine from "../components/Route";
import Status from "../components/Status";

const TABS = [
  ["rides", "Seats I've booked"],
  ["offered", "Rides I'm driving"],
  ["rentals", "Rentals"],
  ["washes", "Washes"],
];

function Actions({ kind, booking, reload }) {
  const [error, setError] = useState("");
  const live = ["pending_payment", "confirmed"].includes(booking.status);
  async function cancel() {
    if (!window.confirm("Cancel this booking?")) return;
    try {
      await api(`/me/bookings/${kind}/${booking.id}/cancel`, { method: "POST" });
      reload();
    } catch (e) {
      setError(e.message);
    }
  }
  return (
    <div className="booking-actions">
      {booking.status === "pending_payment" && (
        <PayButton kind={kind} bookingId={booking.id} amount={booking.total_amount} onPaid={reload} className="btn btn-primary btn-sm" />
      )}
      {live && <button className="btn btn-ghost btn-sm" onClick={cancel}>Cancel booking</button>}
      {error && <p className="form-error">{error}</p>}
    </div>
  );
}

export default function MyBookings() {
  const [data, setData] = useState(null);
  const [tab, setTab] = useState("rides");
  const [error, setError] = useState("");

  const reload = useCallback(() => api("/me/bookings").then(setData).catch((e) => setError(e.message)), []);
  useEffect(() => {
    reload();
  }, [reload]);

  async function cancelRide(ride) {
    if (!window.confirm("Cancel this ride? Everyone booked on it will be cancelled too.")) return;
    try {
      await api(`/rides/${ride.id}/cancel`, { method: "POST" });
      reload();
    } catch (e) {
      setError(e.message);
    }
  }

  const items = data?.[tab] ?? [];
  return (
    <div className="page">
      <h1>My bookings</h1>
      <div className="tabs" role="tablist">
        {TABS.map(([key, label]) => (
          <button key={key} role="tab" aria-selected={tab === key} className={tab === key ? "active" : ""} onClick={() => setTab(key)}>
            {label}
            {data && <span className="count">{data[key].length}</span>}
          </button>
        ))}
      </div>
      {error && <p className="form-error">{error}</p>}
      {data === null && <p className="muted">Loading…</p>}
      {data && items.length === 0 && (
        <div className="empty">
          {tab === "rides" && <p>You haven't booked a seat yet. <Link to="/carpool">Find a ride</Link></p>}
          {tab === "offered" && <p>You haven't offered a ride yet. <Link to="/carpool/offer">Offer a ride</Link></p>}
          {tab === "rentals" && <p>No rentals yet. <Link to="/rent">Rent a car</Link></p>}
          {tab === "washes" && <p>No washes yet. <Link to="/wash">Book a wash</Link></p>}
        </div>
      )}

      <ul className="booking-list">
        {tab === "rides" && items.map((b) => (
          <li key={b.id} className="booking">
            <div>
              <p className="muted">{day(b.ride.depart_at)}, {clock(b.ride.depart_at)}</p>
              <RouteLine from={b.ride.origin} to={b.ride.destination} />
              <p>{b.seats} seat{b.seats > 1 ? "s" : ""} with {b.ride.driver.first_name}. {money(b.total_amount)}</p>
            </div>
            <div className="booking-side"><Status value={b.status} /><Actions kind="ride" booking={b} reload={reload} /></div>
          </li>
        ))}

        {tab === "offered" && items.map((r) => (
          <li key={r.id} className="booking">
            <div>
              <p className="muted">{day(r.depart_at)}, {clock(r.depart_at)}</p>
              <RouteLine from={r.origin} to={r.destination} />
              <p>{r.seats_total - r.seats_available} of {r.seats_total} seats taken at {money(r.price_per_seat)} each</p>
              {r.passengers.length > 0 && (
                <ul className="passengers">
                  {r.passengers.map((p) => (
                    <li key={p.id}>{p.passenger.first_name} {p.passenger.last_name}, {p.seats} seat{p.seats > 1 ? "s" : ""} <Status value={p.status} /></li>
                  ))}
                </ul>
              )}
            </div>
            <div className="booking-side">
              <Status value={r.status} />
              {r.status === "open" && <button className="btn btn-ghost btn-sm" onClick={() => cancelRide(r)}>Cancel ride</button>}
            </div>
          </li>
        ))}

        {tab === "rentals" && items.map((b) => (
          <li key={b.id} className="booking">
            <img src={b.car.image} alt="" className="booking-thumb" />
            <div>
              <p className="strong">{b.car.name}</p>
              <p className="muted">{day(b.pickup_date)}, {b.km} km. {money(b.total_amount)} incl. GST</p>
            </div>
            <div className="booking-side"><Status value={b.status} /><Actions kind="rental" booking={b} reload={reload} /></div>
          </li>
        ))}

        {tab === "washes" && items.map((b) => (
          <li key={b.id} className="booking">
            <div>
              <p className="strong">{b.plan.name} wash at {b.center.name}</p>
              <p className="muted">{day(b.wash_date)}, {slotLabel(b.slot)}, {b.center.area}. {money(b.total_amount)} incl. GST</p>
            </div>
            <div className="booking-side"><Status value={b.status} /><Actions kind="wash" booking={b} reload={reload} /></div>
          </li>
        ))}
      </ul>
    </div>
  );
}
