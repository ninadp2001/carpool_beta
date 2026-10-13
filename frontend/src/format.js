const inr = new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 2 });

/** Amounts come from the API in paise. */
export const money = (paise) => inr.format((paise ?? 0) / 100).replace(/\.00$/, "");
export const toPaise = (rupees) => Math.round(Number(rupees) * 100);

export const day = (d) =>
  new Date(d).toLocaleDateString("en-IN", { weekday: "short", day: "numeric", month: "short" });
export const clock = (d) =>
  new Date(d).toLocaleTimeString("en-IN", { hour: "numeric", minute: "2-digit" });
export const slotLabel = (hhmm) => {
  const [h] = hhmm.split(":").map(Number);
  return `${h % 12 || 12} ${h < 12 ? "am" : "pm"}`;
};

export const todayISO = () => new Date().toLocaleDateString("en-CA");
export const addDaysISO = (n) => {
  const d = new Date();
  d.setDate(d.getDate() + n);
  return d.toLocaleDateString("en-CA");
};

export const STATUS_LABEL = {
  pending_payment: "Awaiting payment",
  confirmed: "Confirmed",
  cancelled: "Cancelled",
  completed: "Completed",
  open: "Open",
  paid: "Paid",
  created: "Started",
  failed: "Failed",
};
