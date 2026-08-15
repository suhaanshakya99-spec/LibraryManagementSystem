// shared helpers used by every page - loaded after config.js

const API_BASE = window.APP_CONFIG.API_BASE;

// --- token storage (member and admin sessions are kept separate) ---

function getToken(role) {
  return localStorage.getItem(role + "_access");
}

function getRefreshToken(role) {
  return localStorage.getItem(role + "_refresh");
}

function saveTokens(role, access, refresh) {
  if (access) localStorage.setItem(role + "_access", access);
  if (refresh) localStorage.setItem(role + "_refresh", refresh);
}

function clearTokens(role) {
  localStorage.removeItem(role + "_access");
  localStorage.removeItem(role + "_refresh");
}

// --- decode a JWT just to read its payload (not for trusting/validating it) ---

function decodeJwt(token) {
  try {
    const part = token.split(".")[1];
    const json = atob(part.replace(/-/g, "+").replace(/_/g, "/"));
    return JSON.parse(json);
  } catch (e) {
    return null;
  }
}

// --- refresh an expired access token ---

async function refreshMemberToken() {
  const refresh = getRefreshToken("member");
  if (!refresh) return false;

  const res = await fetch(API_BASE + "/library/member/login/refresh_token_verify?data=" + encodeURIComponent(refresh), {
    method: "POST",
  });
  if (!res.ok) return false;

  const data = await res.json();
  saveTokens("member", data.access_token, null);
  return true;
}

async function refreshAdminToken() {
  const refresh = getRefreshToken("admin");
  if (!refresh) return false;

  const res = await fetch(API_BASE + "/library/admin/login/verify_refresh_token?token=" + encodeURIComponent(refresh), {
    method: "POST",
  });
  if (!res.ok) return false;

  const data = await res.json();
  saveTokens("admin", data.admin_access_token, null);
  return true;
}

// main request function - role is "member"/"admin"/blank, formEncoded is only for the login endpoints

async function apiRequest(path, method, body, role, formEncoded) {
  const headers = {};
  let fetchBody;

  if (body) {
    if (formEncoded) {
      headers["Content-Type"] = "application/x-www-form-urlencoded";
      fetchBody = new URLSearchParams(body).toString();
    } else {
      headers["Content-Type"] = "application/json";
      fetchBody = JSON.stringify(body);
    }
  }

  if (role) {
    const token = getToken(role);
    if (token) headers["Authorization"] = "Bearer " + token;
  }

  let res = await fetch(API_BASE + path, { method: method, headers: headers, body: fetchBody });

  // access token expired - try to refresh once and retry the request
  if (res.status === 401 && role) {
    const refreshed = role === "member" ? await refreshMemberToken() : await refreshAdminToken();
    if (refreshed) {
      headers["Authorization"] = "Bearer " + getToken(role);
      res = await fetch(API_BASE + path, { method: method, headers: headers, body: fetchBody });
    } else {
      clearTokens(role);
      window.location.href = "login.html";
      return;
    }
  }

  const text = await res.text();
  let data = null;
  if (text) {
    try {
      data = JSON.parse(text);
    } catch (e) {
      data = text;
    }
  }

  if (!res.ok) {
    const message = (data && data.detail) || res.statusText || "Something went wrong";
    throw new Error(typeof message === "string" ? message : JSON.stringify(message));
  }

  return data;
}

// --- route guards, call these at the top of a protected page ---

function requireMemberAuth() {
  if (!getToken("member")) window.location.href = "login.html";
}

function requireAdminAuth() {
  if (!getToken("admin")) window.location.href = "login.html";
}

function signOut(role) {
  clearTokens(role);
  window.location.href = "login.html";
}

// --- small UI helpers ---

function toast(message, type) {
  let host = document.getElementById("toast-host");
  if (!host) {
    host = document.createElement("div");
    host.id = "toast-host";
    document.body.appendChild(host);
  }
  const el = document.createElement("div");
  el.className = "toast toast--" + (type || "info");
  el.textContent = message;
  host.appendChild(el);
  setTimeout(() => el.classList.add("toast--show"), 10);
  setTimeout(() => {
    el.classList.remove("toast--show");
    setTimeout(() => el.remove(), 300);
  }, 3800);
}

function formatDate(value) {
  if (!value) return "—";
  const date = new Date(value);
  if (isNaN(date)) return value;
  return date.toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" });
}

function escapeHtml(value) {
  if (value === null || value === undefined) return "";
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

// renders the rotated "stamp" badge used for every status value
function stampBadge(status) {
  const cls = String(status || "").toLowerCase();
  return '<span class="stamp stamp--' + cls + '">' + escapeHtml(status) + "</span>";
}
