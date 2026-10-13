import { useState } from "react";
import { api } from "../api";
import { money } from "../format";

let scriptPromise;
function loadRazorpay() {
  scriptPromise ??= new Promise((resolve, reject) => {
    const s = document.createElement("script");
    s.src = "https://checkout.razorpay.com/v1/checkout.js";
    s.onload = resolve;
    s.onerror = () => {
      scriptPromise = null;
      reject(new Error("Couldn't load Razorpay. Check your connection."));
    };
    document.body.appendChild(s);
  });
  return scriptPromise;
}

/**
 * Starts payment for a booking. The amount shown is the one the server stored;
 * the server creates the order, and only a verified signature confirms the booking.
 */
export default function PayButton({ kind, bookingId, amount, onPaid, className = "btn btn-primary" }) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [mockOrder, setMockOrder] = useState(null);

  async function start() {
    setBusy(true);
    setError("");
    try {
      const order = await api("/payments/order", { method: "POST", body: { kind, booking_id: bookingId } });
      if (order.mode === "mock") {
        setMockOrder(order);
        return;
      }
      await loadRazorpay();
      const rzp = new window.Razorpay({
        key: order.key_id,
        order_id: order.order_id,
        amount: order.amount,
        currency: order.currency,
        name: "CarPool",
        description: order.description,
        prefill: order.prefill,
        theme: { color: "#22262B" },
        handler: async (res) => {
          try {
            await api("/payments/verify", { method: "POST", body: res });
            onPaid?.();
          } catch (e) {
            setError(e.message);
          }
        },
        modal: { ondismiss: () => setBusy(false) },
      });
      rzp.on("payment.failed", (r) => setError(r.error?.description || "Payment failed. Try another method."));
      rzp.open();
    } catch (e) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  }

  async function completeMock() {
    setBusy(true);
    try {
      await api("/payments/mock/complete", { method: "POST", body: { order_id: mockOrder.order_id } });
      setMockOrder(null);
      onPaid?.();
    } catch (e) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <>
      <button type="button" className={className} onClick={start} disabled={busy}>
        {busy ? "Opening payment…" : `Pay ${money(amount)}`}
      </button>
      {error && <p className="form-error" role="alert">{error}</p>}
      {mockOrder && (
        <div className="dialog-backdrop" role="dialog" aria-modal="true" aria-labelledby="mock-title">
          <div className="dialog">
            <h2 id="mock-title">Test payment</h2>
            <p className="muted">
              Razorpay keys aren't set, so this is a simulated payment. No money moves.
            </p>
            <dl className="summary">
              <div><dt>For</dt><dd>{mockOrder.description}</dd></div>
              <div><dt>Amount</dt><dd className="strong">{money(mockOrder.amount)}</dd></div>
            </dl>
            <div className="row-gap">
              <button className="btn btn-primary" onClick={completeMock} disabled={busy}>
                {busy ? "Paying…" : `Pay ${money(mockOrder.amount)}`}
              </button>
              <button className="btn btn-ghost" onClick={() => setMockOrder(null)} disabled={busy}>
                Not now
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
