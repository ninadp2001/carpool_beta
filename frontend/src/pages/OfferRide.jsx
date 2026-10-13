import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api } from "../api";
import { addDaysISO, money, toPaise } from "../format";

export default function OfferRide() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    origin: "", destination: "", date: addDaysISO(1), time: "08:00",
    seats_total: 3, price: 150, vehicle: "", notes: "",
  });
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(e) {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      const ride = await api("/rides", {
        method: "POST",
        body: {
          origin: form.origin,
          destination: form.destination,
          depart_at: new Date(`${form.date}T${form.time}`).toISOString(),
          seats_total: Number(form.seats_total),
          price_per_seat: toPaise(form.price),
          vehicle: form.vehicle || null,
          notes: form.notes || null,
        },
      });
      navigate(`/carpool?ride=${ride.id}`);
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });
  const seats = Number(form.seats_total) || 0;
  return (
    <div className="page narrow">
      <p><Link to="/carpool">Back to shared rides</Link></p>
      <h1>Offer a ride</h1>
      <p className="lede">Post your trip and the seats you can spare. Riders pay when they book, and you'll see them under My bookings.</p>
      <form className="stack" onSubmit={submit}>
        <div className="grid-2">
          <label className="field"><span>Leaving from</span><input required minLength={2} placeholder="e.g. Thane West" value={form.origin} onChange={set("origin")} /></label>
          <label className="field"><span>Going to</span><input required minLength={2} placeholder="e.g. BKC" value={form.destination} onChange={set("destination")} /></label>
        </div>
        <div className="grid-2">
          <label className="field"><span>Date</span><input type="date" required min={addDaysISO(0)} value={form.date} onChange={set("date")} /></label>
          <label className="field"><span>Departure time</span><input type="time" required value={form.time} onChange={set("time")} /></label>
        </div>
        <div className="grid-2">
          <label className="field"><span>Seats to offer</span><input type="number" min={1} max={8} required value={form.seats_total} onChange={set("seats_total")} /></label>
          <label className="field"><span>Price per seat (₹)</span><input type="number" min={0} max={5000} step="10" required value={form.price} onChange={set("price")} /></label>
        </div>
        <label className="field"><span>Car <small>(optional)</small></span><input placeholder="e.g. Hyundai Creta, grey" value={form.vehicle} onChange={set("vehicle")} /></label>
        <label className="field"><span>Note for riders <small>(optional)</small></span><textarea rows={3} maxLength={500} placeholder="Pick-up point, luggage space, stops on the way" value={form.notes} onChange={set("notes")} /></label>
        <p className="muted">If every seat fills, riders pay {money(toPaise(form.price) * seats)} in total, before GST.</p>
        {error && <p className="form-error" role="alert">{error}</p>}
        <button className="btn btn-primary" disabled={busy}>{busy ? "Posting…" : "Post ride"}</button>
      </form>
    </div>
  );
}
