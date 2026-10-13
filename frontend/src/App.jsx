import { NavLink, Route, Routes, Link, useNavigate } from "react-router-dom";
import { useAuth } from "./auth";
import RequireAuth from "./components/RequireAuth";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Rent from "./pages/Rent";
import Wash from "./pages/Wash";
import Carpool from "./pages/Carpool";
import OfferRide from "./pages/OfferRide";
import MyBookings from "./pages/MyBookings";
import Admin from "./pages/admin/Admin";

function Header() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  return (
    <header className="site-header">
      <div className="site-header-inner">
        <Link to="/" className="wordmark" aria-label="CarPool home">
          Car<span>Pool</span>
        </Link>
        <nav className="main-nav" aria-label="Main">
          <NavLink to="/carpool">Shared rides</NavLink>
          <NavLink to="/rent">Rent a car</NavLink>
          <NavLink to="/wash">Car wash</NavLink>
        </nav>
        <div className="account-nav">
          {user ? (
            <>
              {user.is_admin && <NavLink to="/admin">Admin</NavLink>}
              <NavLink to="/bookings">My bookings</NavLink>
              <button
                className="link-button"
                onClick={() => {
                  logout();
                  navigate("/");
                }}
              >
                Log out
              </button>
            </>
          ) : (
            <>
              <NavLink to="/login">Log in</NavLink>
              <Link to="/register" className="btn btn-primary btn-sm">Sign up</Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
}

export default function App() {
  return (
    <>
      <a href="#main" className="skip-link">Skip to content</a>
      <Header />
      <main id="main">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/rent" element={<Rent />} />
          <Route path="/wash" element={<Wash />} />
          <Route path="/carpool" element={<Carpool />} />
          <Route path="/carpool/offer" element={<RequireAuth><OfferRide /></RequireAuth>} />
          <Route path="/bookings" element={<RequireAuth><MyBookings /></RequireAuth>} />
          <Route path="/admin/*" element={<RequireAuth admin><Admin /></RequireAuth>} />
          <Route path="*" element={<div className="page"><h1>Page not found</h1><Link to="/">Go to the home page</Link></div>} />
        </Routes>
      </main>
      <footer className="site-footer">
        <p>CarPool, Mumbai. A portfolio project by Ninad Patil.</p>
      </footer>
    </>
  );
}
