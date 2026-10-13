import { useEffect, useState } from "react";
import { api } from "../../api";
import { money, toPaise } from "../../format";

/** List + add/edit form for cars, wash plans and wash centres. Items are hidden, never deleted. */
export default function Catalog({ title, path, fields }) {
  const [rows, setRows] = useState(null);
  const [editing, setEditing] = useState(null); // null = closed, {} = new, row = edit
  const [form, setForm] = useState({});
  const [error, setError] = useState("");

  const load = () => api(`/admin/${path}`).then(setRows).catch((e) => setError(e.message));
  useEffect(() => {
    setRows(null);
    setEditing(null);
    load();
  }, [path]); // eslint-disable-line react-hooks/exhaustive-deps

  function open(row) {
    const f = {};
    for (const { key, type } of fields) {
      const v = row[key];
      f[key] = type === "money" ? (v ?? 0) / 100 : type === "lines" ? (v ?? []).join("\n") : v ?? "";
    }
    f.is_active = row.is_active ?? true;
    setForm(f);
    setEditing(row);
    setError("");
  }

  async function save(e) {
    e.preventDefault();
    const body = { is_active: form.is_active };
    for (const { key, type } of fields) {
      const v = form[key];
      body[key] =
        type === "money" ? toPaise(v)
        : type === "number" ? Number(v)
        : type === "lines" ? String(v).split("\n").map((x) => x.trim()).filter(Boolean)
        : v === "" ? null : v;
    }
    try {
      await api(editing.id ? `/admin/${path}/${editing.id}` : `/admin/${path}`, { method: editing.id ? "PUT" : "POST", body });
      setEditing(null);
      load();
    } catch (err) {
      setError(err.message);
    }
  }

  const display = (row, { key, type }) =>
    type === "money" ? money(row[key]) : type === "lines" ? `${row[key].length} items` : row[key];
  const shown = fields.filter((f) => f.type !== "textarea").slice(0, 4);

  return (
    <>
      <div className="title-row">
        <h1>{title}</h1>
        <button className="btn btn-primary" onClick={() => open({})}>Add new</button>
      </div>
      {error && !editing && <p className="form-error">{error}</p>}

      {editing && (
        <form className="panel stack admin-form" onSubmit={save}>
          <h2>{editing.id ? `Edit ${editing.name}` : "Add new"}</h2>
          <div className="grid-2">
            {fields.map(({ key, label, type, placeholder }) => (
              <label key={key} className={`field${type === "textarea" || type === "lines" ? " span-2" : ""}`}>
                <span>{label}</span>
                {type === "textarea" || type === "lines" ? (
                  <textarea rows={type === "lines" ? 5 : 3} value={form[key]} onChange={(e) => setForm({ ...form, [key]: e.target.value })} />
                ) : (
                  <input
                    type={type === "money" || type === "number" ? "number" : "text"}
                    step={type === "money" ? "0.01" : undefined}
                    required={key === "name" || type === "money" || type === "number"}
                    placeholder={placeholder}
                    value={form[key]}
                    onChange={(e) => setForm({ ...form, [key]: e.target.value })}
                  />
                )}
              </label>
            ))}
          </div>
          <label className="check">
            <input type="checkbox" checked={form.is_active} onChange={(e) => setForm({ ...form, is_active: e.target.checked })} />
            Show to customers
          </label>
          {error && <p className="form-error" role="alert">{error}</p>}
          <div className="row-gap">
            <button className="btn btn-primary">Save</button>
            <button type="button" className="btn btn-ghost" onClick={() => setEditing(null)}>Discard</button>
          </div>
        </form>
      )}

      <div className="table-wrap">
        <table className="table">
          <thead>
            <tr>{shown.map((f) => <th key={f.key}>{f.label}</th>)}<th>Visible</th><th /></tr>
          </thead>
          <tbody>
            {rows?.map((r) => (
              <tr key={r.id} className={r.is_active ? "" : "inactive"}>
                {shown.map((f) => <td key={f.key}>{display(r, f)}</td>)}
                <td>{r.is_active ? "Yes" : "Hidden"}</td>
                <td className="row-actions"><button className="btn btn-ghost btn-sm" onClick={() => open(r)}>Edit</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
