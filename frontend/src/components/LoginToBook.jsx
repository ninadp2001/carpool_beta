import { Link, useLocation } from "react-router-dom";

export default function LoginToBook() {
  const location = useLocation();
  return (
    <p className="muted">
      <Link to="/login" state={{ from: location.pathname + location.search }}>Log in</Link> or{" "}
      <Link to="/register" state={{ from: location.pathname + location.search }}>create an account</Link> to book.
    </p>
  );
}
