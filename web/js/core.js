window.Paakat = (function () {
  const $ = (id) => document.getElementById(id);

  const API_PORT = "8010";
  const STORED_API = localStorage.getItem("paakat_api");
  const DEFAULT_API = STORED_API || (
    location.protocol.startsWith("http")
      ? location.protocol + "//" + location.hostname + ":" + API_PORT
      : "http://127.0.0.1:" + API_PORT
  );

  function apiBase() {
    const value = ($("apiBase").value || DEFAULT_API).trim();
    return value.replace(/\/+$/, "");
  }

  function showHint(text, isError) {
    const hint = $("hint");
    hint.textContent = text;
    hint.classList.toggle("error", !!isError);
  }

  function escapeHtml(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function deviceId() {
    let id = localStorage.getItem("paakat_device");
    if (!id) {
      id = "web-" + (crypto.randomUUID ? crypto.randomUUID() : Math.random().toString(36).slice(2));
      localStorage.setItem("paakat_device", id);
    }
    return id;
  }

  return { $, apiBase, showHint, escapeHtml, deviceId, DEFAULT_API };
})();
