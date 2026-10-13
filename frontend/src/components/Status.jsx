import { STATUS_LABEL } from "../format";

export default function Status({ value }) {
  return <span className={`status status-${value}`}>{STATUS_LABEL[value] ?? value}</span>;
}
