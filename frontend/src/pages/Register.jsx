import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { api } from "../api";
import { useAuth } from "../auth";

export default function Register() {
  const { signIn } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [form, setForm] = useState({ first_name: "", last_name: "", email: "", phone: "", password: "" });
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(e) {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      signIn(await api("/auth/register", { method: "POST", body: form }));
      navigate(location.state?.from || "/", { replace: true });
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });
  return (
    <div className="page narrow">
      <h1>Create an account</h1>
      <form onSubmit={submit} className="stack">
        <div className="grid-2">
          <label className="field">
            <span>First name</span>
            <input autoComplete="given-name" required minLength={2} value={form.first_name} onChange={set("first_name")} />
          </label>
          <label className="field">
            <span>Last name</span>
            <input autoComplete="family-name" required value={form.last_name} onChange={set("last_name")} />
          </label>
        </div>
        <label className="field">
          <span>Email</span>
          <input type="email" autoComplete="email" required value={form.email} onChange={set("email")} />
        </label>
        <label className="field">
          <span>Mobile number <small>(optional)</small></span>
          <input type="tel" autoComplete="tel" inputMode="tel" value={form.phone} onChange={set("phone")} />
        </label>
        <label className="field">
          <span>Password</span>
          <input type="password" autoComplete="new-password" required minLength={8} value={form.password} onChange={set("password")} aria-describedby="pw-hint" />
          <small id="pw-hint" className="muted">At least 8 characters, with an uppercase letter, a lowercase letter and a number.</small>
        </label>
        {error && <p className="form-error" role="alert">{error}</p>}
        <button className="btn btn-primary" disabled={busy}>{busy ? "Creating account…" : "Create account"}</button>
      </form>
      <p className="muted">Already have an account? <Link to="/login" state={location.state}>Log in</Link></p>
    </div>
  );
}
