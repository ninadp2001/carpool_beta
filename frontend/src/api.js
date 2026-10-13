const BASE = (import.meta.env.VITE_API_URL || "") + "/api";
const TOKEN_KEY = "carpool_token";

export const token = {
  get: () => localStorage.getItem(TOKEN_KEY),
  set: (t) => localStorage.setItem(TOKEN_KEY, t),
  clear: () => localStorage.removeItem(TOKEN_KEY),
};

export class ApiError extends Error {
  constructor(status, message) {
    super(message);
    this.status = status;
  }
}

// FastAPI returns {detail: "..."} or, for validation errors, {detail: [{loc, msg}, ...]}.
function messageFrom(body, status) {
  const d = body?.detail;
  if (typeof d === "string") return d;
  if (Array.isArray(d) && d.length) {
    const field = d[0].loc?.[d[0].loc.length - 1];
    const msg = d[0].msg.replace(/^Value error, /, "");
    return field && field !== "body" ? `${field.replace(/_/g, " ")}: ${msg}` : msg;
  }
  return status >= 500 ? "Something went wrong on our side. Try again." : "Request failed";
}

export async function api(path, { method = "GET", body, params } = {}) {
  const url = new URL(BASE + path, window.location.origin);
  if (params) Object.entries(params).forEach(([k, v]) => v !== "" && v != null && url.searchParams.set(k, v));
  const headers = { "Content-Type": "application/json" };
  const t = token.get();
  if (t) headers.Authorization = `Bearer ${t}`;

  let res;
  try {
    res = await fetch(url, { method, headers, body: body ? JSON.stringify(body) : undefined });
  } catch {
    throw new ApiError(0, "Can't reach the server. Check your connection.");
  }
  const data = res.status === 204 ? null : await res.json().catch(() => null);
  if (!res.ok) {
    if (res.status === 401) window.dispatchEvent(new Event("carpool:logout"));
    throw new ApiError(res.status, messageFrom(data, res.status));
  }
  return data;
}
