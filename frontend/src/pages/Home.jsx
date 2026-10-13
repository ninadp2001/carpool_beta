import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";
import { clock, day, money } from "../format";
import RouteLine from "../components/Route";

export default function Home() {
  const [rides, setRides] = useState(null);

  useEffect(() => {
    api("/rides").then((r) => setRides(r.slice(0, 4))).catch(() => setRides([]));
  }, []);

  return (
    <>
      <section className="hero">
        <div className="hero-inner">
          <div className="hero-copy">
            <h1>Share the drive across Mumbai.</h1>
            <p className="lede">
              Find a seat in someone's car going your way, or offer the empty seats in yours.
              Need the whole car? Rent one by the kilometre, and book a wash when you bring it back.
            </p>
            <div className="row-gap">
              <Link to="/carpool" className="btn btn-primary btn-lg">Find a ride</Link>
              <Link to="/carpool/offer" className="btn btn-outline-light btn-lg">Offer a ride</Link>
            </div>
          </div>

          <div className="departures" aria-labelledby="departures-title">
            <h2 id="departures-title">Leaving soon</h2>
            {rides === null && <p className="muted-light">Loading rides…</p>}
            {rides?.length === 0 && (
              <p className="muted-light">No rides posted yet. <Link to="/carpool/offer">Post the first one.</Link></p>
            )}
            <ul>
              {rides?.map((r) => (
                <li key={r.id}>
                  <Link to={`/carpool?ride=${r.id}`} className="departure">
                    <span className="departure-time">
                      <strong>{clock(r.depart_at)}</strong>
                      {day(r.depart_at)}
                    </span>
                    <RouteLine from={r.origin} to={r.destination} size="sm" />
                    <span className="departure-meta">
                      {money(r.price_per_seat)}
                      <small>{r.seats_available} left</small>
                    </span>
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </section>

      <section className="page services">
        <article className="service">
          <h2>Shared rides</h2>
          <p>Split the fuel on your commute or a weekend trip to Pune or Nashik. Book a seat, pay online, and the driver sees you on their list.</p>
          <Link to="/carpool">Search rides</Link>
        </article>
        <article className="service">
          <h2>Rent a car</h2>
          <p>Eight cars from a WagonR to a 17-seat Tempo Traveller. You pay per kilometre, and you see the full price with GST before you book.</p>
          <Link to="/rent">See the cars</Link>
        </article>
        <article className="service">
          <h2>Car wash</h2>
          <p>Three plans at ten centres from Colaba to Kharghar. Pick a time slot that's still open and pay when you book.</p>
          <Link to="/wash">Book a wash</Link>
        </article>
      </section>
    </>
  );
}
