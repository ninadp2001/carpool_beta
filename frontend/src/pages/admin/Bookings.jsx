import { useEffect, useState } from "react";
import { api } from "../../api";
import { clock, day, money, slotLabel } from "../../format";
import Status from "../../components/Status";

const KINDS = { ride: "Shared rides", rental: "Rentals", wash: "Washes" };

function describe(kind, b) {
  if (kind === "rental") return [b.car.name, `${day(b.pickup_date)}, ${b.km} km`];
  if (kind === "wash") return [`${b.plan.name} at ${b.center.name}`, `${day(b.wash_date)}, ${slotLabel(b.slot)}`];
  return [`${b.ride.origin} to ${b.ride.destination}`, `${day(b.ride.depart_at)}, ${clock(b.ride.depart_at)}, ${b.seats} seat(s)`];
}

export default function Bookings() {
  const [kind, setKind] = useState("ride");
  const [status, setStatus] = useState("");
  const [rows, setRows] = useState(null);
  const [error, setError] = useState("");

  const load = () => api(`/admin/bookings/${kind}`, { params: { status } }).then(setRows).catch((e) => setError(e.message));
  useEffect(() => {
    setRows(null);
    load();
  }, [kind, status]); // eslint-disable-line react-hooks/exhaustive-deps

  async function update(id, next) {
    if (next === "cancelled" && !window.confirm("Cancel this booking? Refund any payment from the Razorpay dashboard.")) return;
    try {
      await api(`/admin/bookings/${kind}/${id}`, { method: "PATCH", body: { status: next } });
      load();
    } catch (e) {
      setError(e.message);
    }
  }

  return (
    <>
      <h1>Bookings</h1>
      <div className="row-gap filters">
        <div className="tabs" role="tablist">
          {Object.entries(KINDS).map(([k, label]) => (
            <button key={k} role="tab" aria-selected={kind === k} className={kind === k ? "active" : ""} onClick={() => setKind(k)}>{label}</button>
          ))}
        </div>
        <label className="field inline-field">
          <span>Status</span>
          <select value={status} onChange={(e) => setStatus(e.target.value)}>
            <option value="">All</option>
            <option value="pending_payment">Awaiting payment</option>
            <option value="confirmed">Confirmed</option>
            <option value="completed">Completed</option>
            <option value="cancelled">Cancelled</option>
          </select>
        </label>
      </div>
      {error && <p className="form-error">{error}</p>}
      <div className="table-wrap">
        <table className="table">
          <thead><tr><th>#</th><th>Customer</th><th>Booking</th><th>When</th><th className="num">Amount</th><th>Status</th><th /></tr></thead>
          <tbody>
            {rows?.map((b) => {
              const [what, when] = describe(kind, b);
              const who = b.user ?? b.passenger;
              return (
                <tr key={b.id}>
                  <td>{b.id}</td><td>{who.first_name} {who.last_name}<br /><small className="muted">{who.email}</small></td><td>{what}</td><td>{when}</td><td className="num">{money(b.total_amount)}</td>
                  <td><Status value={b.status} /></td>
                  <td className="row-actions">
                    {b.status === "confirmed" && <button className="btn btn-ghost btn-sm" onClick={() => update(b.id, "completed")}>Mark completed</button>}
                    {["confirmed", "pending_payment"].includes(b.status) && <button className="btn btn-ghost btn-sm" onClick={() => update(b.id, "cancelled")}>Cancel</button>}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
        {rows?.length === 0 && <p className="muted empty">No bookings here.</p>}
      </div>
    </>
  );
}
