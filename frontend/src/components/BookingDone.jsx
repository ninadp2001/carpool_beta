import { Link } from "react-router-dom";

export default function BookingDone({ title, children }) {
  return (
    <div className="done" role="status">
      <h3>{title}</h3>
      {children && <p>{children}</p>}
      <Link to="/bookings">View my bookings</Link>
    </div>
  );
}
