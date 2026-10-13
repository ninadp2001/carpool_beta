/** The lane-line route mark: origin, a dashed road, destination. Used across carpool screens. */
export default function RouteLine({ from, to, size = "md" }) {
  return (
    <div className={`route route-${size}`}>
      <span className="route-stop">{from}</span>
      <span className="route-road" aria-hidden="true" />
      <span className="route-stop">{to}</span>
      <span className="sr-only">{`${from} to ${to}`}</span>
    </div>
  );
}
