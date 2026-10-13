import { useEffect, useState } from "react";
import { api } from "../../api";
import { clock, day, money } from "../../format";
import Status from "../../components/Status";

function useList(path, params) {
  const [rows, setRows] = useState(null);
  const [error, setError] = useState("");
  const key = JSON.stringify(params ?? {});
  const load = () => api(path, { params }).then(setRows).catch((e) => setError(e.message));
  useEffect(() => {
    load();
  }, [path, key]); // eslint-disable-line react-hooks/exhaustive-deps
  return { rows, error, setError, load };
}

export function Users() {
  const [q, setQ] = useState("");
  const [search, setSearch] = useState("");
  const { rows, error } = useList("/admin/users", { q: search });
  return (
    <>
      <h1>Users</h1>
      <form className="row-gap filters" onSubmit={(e) => { e.preventDefault(); setSearch(q); }} role="search">
        <input aria-label="Search users" placeholder="Name or email" value={q} onChange={(e) => setQ(e.target.value)} />
        <button className="btn btn-outline btn-sm">Search</button>
      </form>
      {error && <p className="form-error">{error}</p>}
      <div className="table-wrap">
        <table className="table">
          <thead><tr><th>Name</th><th>Email</th><th>Phone</th><th>Joined</th><th>Role</th></tr></thead>
          <tbody>
            {rows?.map((u) => (
              <tr key={u.id}>
                <td>{u.first_name} {u.last_name}</td><td>{u.email}</td><td>{u.phone ?? "–"}</td>
                <td>{day(u.created_at)}</td><td>{u.is_admin ? "Admin" : "Customer"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}

export function Rides() {
  const { rows, error, setError, load } = useList("/admin/rides");
  async function cancel(id) {
    if (!window.confirm("Cancel this ride and every booking on it?")) return;
    try {
      await api(`/admin/rides/${id}/cancel`, { method: "POST" });
      load();
    } catch (e) {
      setError(e.message);
    }
  }
  return (
    <>
      <h1>Shared rides</h1>
      {error && <p className="form-error">{error}</p>}
      <div className="table-wrap">
        <table className="table">
          <thead><tr><th>Route</th><th>Driver</th><th>Departs</th><th>Seats taken</th><th className="num">Per seat</th><th>Status</th><th /></tr></thead>
          <tbody>
            {rows?.map((r) => (
              <tr key={r.id}>
                <td>{r.origin} to {r.destination}</td>
                <td>{r.driver.first_name} {r.driver.last_name}</td>
                <td>{day(r.depart_at)}, {clock(r.depart_at)}</td>
                <td>{r.seats_total - r.seats_available} / {r.seats_total}</td>
                <td className="num">{money(r.price_per_seat)}</td>
                <td><Status value={r.status} /></td>
                <td className="row-actions">{r.status === "open" && <button className="btn btn-ghost btn-sm" onClick={() => cancel(r.id)}>Cancel</button>}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}

export function Payments() {
  const { rows, error } = useList("/admin/payments");
  return (
    <>
      <h1>Payments</h1>
      <p className="muted">Refunds are issued from the Razorpay dashboard using the payment ID.</p>
      {error && <p className="form-error">{error}</p>}
      <div className="table-wrap">
        <table className="table">
          <thead><tr><th>Date</th><th>For</th><th>Order ID</th><th>Payment ID</th><th className="num">Amount</th><th>Status</th></tr></thead>
          <tbody>
            {rows?.map((p) => (
              <tr key={p.id}>
                <td>{day(p.created_at)}</td>
                <td>{p.booking_kind} #{p.booking_id}</td>
                <td><code>{p.order_id}</code></td>
                <td><code>{p.payment_id ?? "–"}</code></td>
                <td className="num">{money(p.amount)}</td>
                <td><Status value={p.status} /></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
