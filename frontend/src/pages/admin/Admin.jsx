import { NavLink, Navigate, Route, Routes } from "react-router-dom";
import Overview from "./Overview";
import Bookings from "./Bookings";
import Catalog from "./Catalog";
import { Payments, Rides, Users } from "./Lists";

const CAR_FIELDS = [
  { key: "name", label: "Name" },
  { key: "seats", label: "Seats", type: "number" },
  { key: "rate_per_km", label: "Rate per km (₹)", type: "money" },
  { key: "image", label: "Image path", placeholder: "/cars/verna.jpg" },
];
const PLAN_FIELDS = [
  { key: "name", label: "Name" },
  { key: "price", label: "Price (₹)", type: "money" },
  { key: "features", label: "Included (one per line)", type: "lines" },
];
const CENTER_FIELDS = [
  { key: "name", label: "Name" },
  { key: "area", label: "Area" },
  { key: "address", label: "Address", type: "textarea" },
  { key: "phone", label: "Phone" },
  { key: "slot_capacity", label: "Cars per time slot", type: "number" },
];

const LINKS = [
  ["", "Overview"], ["bookings", "Bookings"], ["payments", "Payments"], ["rides", "Shared rides"],
  ["cars", "Cars"], ["plans", "Wash plans"], ["centers", "Wash centres"], ["users", "Users"],
];

export default function Admin() {
  return (
    <div className="admin">
      <nav className="admin-nav" aria-label="Admin">
        {LINKS.map(([to, label]) => (
          <NavLink key={to} to={to} end={to === ""}>{label}</NavLink>
        ))}
      </nav>
      <section className="admin-body">
        <Routes>
          <Route index element={<Overview />} />
          <Route path="bookings" element={<Bookings />} />
          <Route path="payments" element={<Payments />} />
          <Route path="rides" element={<Rides />} />
          <Route path="cars" element={<Catalog title="Cars" path="cars" fields={CAR_FIELDS} />} />
          <Route path="plans" element={<Catalog title="Wash plans" path="plans" fields={PLAN_FIELDS} />} />
          <Route path="centers" element={<Catalog title="Wash centres" path="centers" fields={CENTER_FIELDS} />} />
          <Route path="users" element={<Users />} />
          <Route path="*" element={<Navigate to="/admin" replace />} />
        </Routes>
      </section>
    </div>
  );
}
