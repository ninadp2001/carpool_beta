import { useEffect, useState } from "react";
import { api } from "../api";
import { useAuth } from "../auth";
import { addDaysISO, day, money, slotLabel, todayISO } from "../format";
import PayButton from "../components/PayButton";
import BookingDone from "../components/BookingDone";
import LoginToBook from "../components/LoginToBook";

export default function Wash() {
  const { user } = useAuth();
  const [plans, setPlans] = useState([]);
  const [centers, setCenters] = useState([]);
  const [planId, setPlanId] = useState(null);
  const [centerId, setCenterId] = useState("");
  const [date, setDate] = useState(addDaysISO(1));
  const [slots, setSlots] = useState(null);
  const [slot, setSlot] = useState(null);
  const [booking, setBooking] = useState(null);
  const [paid, setPaid] = useState(false);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    api("/wash/plans").then((p) => {
      setPlans(p);
      setPlanId(p[1]?.id ?? p[0]?.id);
    });
    api("/wash/centers").then(setCenters);
  }, []);

  useEffect(() => {
    setSlot(null);
    setSlots(null);
    if (!centerId || !date) return;
    api(`/wash/centers/${centerId}/slots`, { params: { day: date } }).then(setSlots).catch((e) => setError(e.message));
  }, [centerId, date]);

  const plan = plans.find((p) => p.id === planId);
  const center = centers.find((c) => c.id === Number(centerId));
  const allFeatures = plans.at(-1)?.features ?? [];

  async function book() {
    setBusy(true);
    setError("");
    try {
      setBooking(await api("/wash/bookings", { method: "POST", body: { plan_id: planId, center_id: Number(centerId), wash_date: date, slot } }));
    } catch (err) {
      setError(err.message);
      if (err.status === 409) api(`/wash/centers/${centerId}/slots`, { params: { day: date } }).then(setSlots);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="page">
      <h1>Car wash</h1>
      <p className="lede">Pick a plan, a centre near you and a time. Prices include everything listed; GST is added at checkout.</p>

      <fieldset className="plans">
        <legend className="step-title">Plan</legend>
        {plans.map((p) => (
          <label key={p.id} className={`plan${planId === p.id ? " selected" : ""}`}>
            <input type="radio" name="plan" checked={planId === p.id} onChange={() => setPlanId(p.id)} />
            <span className="plan-name">{p.name}</span>
            <span className="plan-price">{money(p.price)}</span>
            <ul>
              {allFeatures.map((f) => (
                <li key={f} className={p.features.includes(f) ? "has" : "not"}>
                  <span className="sr-only">{p.features.includes(f) ? "Included: " : "Not included: "}</span>
                  {f}
                </li>
              ))}
            </ul>
          </label>
        ))}
      </fieldset>

      <div className="split wash-split">
        <div className="stack">
          <div className="grid-2">
            <label className="field">
              <span className="step-title">Centre</span>
              <select value={centerId} onChange={(e) => setCenterId(e.target.value)}>
                <option value="">Choose a centre</option>
                {centers.map((c) => (
                  <option key={c.id} value={c.id}>{c.area}: {c.name}</option>
                ))}
              </select>
            </label>
            <label className="field">
              <span className="step-title">Date</span>
              <input type="date" min={todayISO()} max={addDaysISO(30)} value={date} onChange={(e) => setDate(e.target.value)} />
            </label>
          </div>
          {center && <p className="muted address">{center.address}{center.phone && `. Phone ${center.phone}`}</p>}

          {centerId && (
            <div>
              <p className="step-title" id="slot-label">Time</p>
              {slots?.length === 0 && <p className="muted">No times left on this day. Try the next day.</p>}
              <div className="slots" role="radiogroup" aria-labelledby="slot-label">
                {slots?.map((s) => (
                  <button
                    key={s.slot}
                    role="radio"
                    aria-checked={slot === s.slot}
                    className={`slot${slot === s.slot ? " selected" : ""}`}
                    disabled={s.available === 0 || !!booking}
                    onClick={() => setSlot(s.slot)}
                  >
                    {slotLabel(s.slot)}
                    <small>{s.available === 0 ? "Full" : `${s.available} open`}</small>
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        <aside className="panel">
          <dl className="summary">
            <div><dt>Plan</dt><dd>{plan?.name ?? "–"}</dd></div>
            <div><dt>Centre</dt><dd>{center?.area ?? "–"}</dd></div>
            <div><dt>When</dt><dd>{slot ? `${day(date)}, ${slotLabel(slot)}` : "–"}</dd></div>
            <div className="total"><dt>Plan price</dt><dd>{plan ? money(plan.price) : "–"}</dd></div>
          </dl>
          {error && <p className="form-error" role="alert">{error}</p>}
          {!user && <LoginToBook />}
          {user && !booking && (
            <button className="btn btn-primary" onClick={book} disabled={busy || !plan || !center || !slot}>
              {busy ? "Booking…" : "Book this slot"}
            </button>
          )}
          {booking && !paid && (
            <div className="stack">
              <p>Slot held for 15 minutes. Total with GST:</p>
              <PayButton kind="wash" bookingId={booking.id} amount={booking.total_amount} onPaid={() => setPaid(true)} />
            </div>
          )}
          {paid && <BookingDone title="Wash booked">{booking.plan.name} at {booking.center.name}, {day(booking.wash_date)} at {slotLabel(booking.slot)}.</BookingDone>}
        </aside>
      </div>
    </div>
  );
}
