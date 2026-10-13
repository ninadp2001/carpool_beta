import { useEffect, useState } from "react";
import { api } from "../../api";
import { money } from "../../format";

const KIND_LABEL = { ride: "Shared rides", rental: "Rentals", wash: "Washes" };

export default function Overview() {
  const [s, setS] = useState(null);
  const [error, setError] = useState("");
  useEffect(() => {
    api("/admin/stats").then(setS).catch((e) => setError(e.message));
  }, []);
  if (error) return <p className="form-error">{error}</p>;
  if (!s) return <p className="muted">Loading…</p>;

  // Fill in days with no payments so the chart always shows 14 bars.
  const byDate = Object.fromEntries(s.revenue_daily.map((d) => [d.date, d.amount]));
  const days = Array.from({ length: 14 }, (_, i) => {
    const d = new Date();
    d.setDate(d.getDate() - 13 + i);
    const iso = d.toLocaleDateString("en-CA");
    return { date: iso, amount: byDate[iso] ?? 0 };
  });
  const max = Math.max(1, ...days.map((d) => d.amount));
  return (
    <>
      <h1>Overview</h1>
      <div className="stat-row">
        <div className="stat stat-lead"><span>Revenue collected</span><strong>{money(s.revenue_total)}</strong></div>
        <div className="stat"><span>Users</span><strong>{s.users}</strong></div>
        <div className="stat"><span>Open rides</span><strong>{s.open_rides}</strong></div>
        <div className="stat"><span>Awaiting payment</span><strong>{s.pending}</strong></div>
      </div>

      <div className="grid-2 admin-grid">
        <div className="panel">
          <h2>Last 14 days</h2>
          {s.revenue_daily.length === 0 ? (
            <p className="muted">No payments in the last two weeks.</p>
          ) : (
            <ul className="bars" aria-label="Revenue per day">
              {days.map((d) => (
                <li key={d.date} title={`${d.date}: ${money(d.amount)}`}>
                  <span className="bar" style={{ height: `${(d.amount / max) * 100}%` }} />
                  <small>{d.date.slice(8)}</small>
                </li>
              ))}
            </ul>
          )}
        </div>
        <div className="panel">
          <h2>By service</h2>
          <table className="table">
            <thead><tr><th>Service</th><th>Confirmed</th><th className="num">Revenue</th></tr></thead>
            <tbody>
              {Object.entries(KIND_LABEL).map(([k, label]) => (
                <tr key={k}><td>{label}</td><td>{s.confirmed[k]}</td><td className="num">{money(s.revenue_by_kind[k])}</td></tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}
