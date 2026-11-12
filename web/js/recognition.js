(function () {
  const { $, apiBase, showHint, escapeHtml, deviceId, DEFAULT_API } = window.Paakat;

  let stream = null;
  let blob = null;
  let blobName = "captura.jpg";
  let previewUrl = null;

  async function startCamera() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      showHint("Este navegador no permite abrir la cámara. Usa Subir imagen.", true);
      return;
    }
    try {
      stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: { ideal: "environment" } },
        audio: false
      });
      const video = $("video");
      video.srcObject = stream;
      video.hidden = false;
      $("preview").hidden = true;
      $("placeholder").hidden = true;
      await video.play();
      $("btnCapture").disabled = false;
      $("btnCamera").disabled = true;
      $("btnCamera").textContent = "Cámara activa";
      showHint("Encuadra el monumento y pulsa “Tomar foto”.");
    } catch (err) {
      showHint("No se pudo abrir la cámara: " + err.message + ". Puedes subir una imagen.", true);
    }
  }

  function capture() {
    const video = $("video");
    if (!video.videoWidth) {
      showHint("La cámara aún no está lista. Espera un momento e inténtalo de nuevo.", true);
      return;
    }
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext("2d").drawImage(video, 0, 0);
    canvas.toBlob((result) => {
      if (result) setBlob(result, "captura.jpg");
    }, "image/jpeg", 0.92);
  }

  function setBlob(nextBlob, name) {
    blob = nextBlob;
    blobName = name || "captura.jpg";
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    previewUrl = URL.createObjectURL(nextBlob);
    $("preview").src = previewUrl;
    $("preview").hidden = false;
    $("video").hidden = true;
    $("placeholder").hidden = true;
    $("btnRecognize").disabled = false;
    showHint("Foto lista. Pulsa “Reconocer sitio”.");
  }

  async function recognize() {
    if (!blob) {
      showHint("Primero toma o sube una foto.", true);
      return;
    }
    const button = $("btnRecognize");
    const previous = button.textContent;
    button.disabled = true;
    button.textContent = "Analizando…";
    showHint("Consultando el modelo…");
    try {
      const form = new FormData();
      form.append("file", blob, blobName);
      form.append("device_id", deviceId());
      const response = await fetch(apiBase() + "/api/v1/recognize", { method: "POST", body: form });
      if (!response.ok) {
        const detail = await response.text();
        throw new Error("HTTP " + response.status + " · " + detail.slice(0, 160));
      }
      const data = await response.json();
      renderResult(data);
      loadHistory();
    } catch (err) {
      showHint("Error al reconocer: " + err.message, true);
    } finally {
      button.disabled = false;
      button.textContent = previous;
    }
  }

  function renderResult(data) {
    const card = $("resultCard");
    const element = data.element;
    const confidence = Math.max(0, Math.min(1, Number(data.confidence) || 0));
    const pct = Math.round(confidence * 100);

    $("resName").textContent = element ? element.name : (data.label || "Desconocido");
    $("resCategory").textContent = element && element.category ? element.category.name : "Sin categoría";
    $("confText").textContent = pct + "%";

    const bar = $("confBar");
    bar.style.width = pct + "%";
    bar.className = confidence >= 0.7 ? "ok" : confidence >= 0.45 ? "mid" : "low";

    const badge = $("statusBadge");
    badge.textContent = data.recognized ? "Sitio identificado" : "Coincidencia baja";
    badge.className = "tag " + (data.recognized ? "ok" : "warn");

    const meta = $("resMeta");
    meta.innerHTML = "";
    const rows = [
      ["Ubicación", element ? element.location : null],
      ["Época", element ? element.era : null]
    ];
    rows.forEach(([label, value]) => {
      if (!value) return;
      const dt = document.createElement("dt");
      dt.textContent = label;
      const dd = document.createElement("dd");
      dd.textContent = value;
      meta.appendChild(dt);
      meta.appendChild(dd);
    });

    $("resDesc").textContent = (element && element.description) || "Sin descripción disponible.";

    const list = $("candidates");
    list.innerHTML = "";
    (data.top_k || []).forEach((candidate) => {
      const candidatePct = Math.round((Number(candidate.confidence) || 0) * 100);
      const item = document.createElement("li");
      const label = document.createElement("span");
      label.className = "cand-label";
      label.textContent = candidate.label;
      const track = document.createElement("span");
      track.className = "cand-bar";
      const fill = document.createElement("i");
      fill.style.width = candidatePct + "%";
      track.appendChild(fill);
      const value = document.createElement("span");
      value.className = "cand-pct";
      value.textContent = candidatePct + "%";
      item.appendChild(label);
      item.appendChild(track);
      item.appendChild(value);
      list.appendChild(item);
    });

    card.hidden = false;
    card.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  async function loadHistory() {
    const list = $("history");
    try {
      const response = await fetch(apiBase() + "/api/v1/recognitions?limit=6");
      if (!response.ok) throw new Error("HTTP " + response.status);
      const rows = await response.json();
      if (!rows.length) {
        list.innerHTML = '<li class="placeholder-row">Aún no hay reconocimientos.</li>';
        return;
      }
      list.innerHTML = rows.map((row, index) => {
        const pct = Math.round((Number(row.confidence) || 0) * 100);
        const when = row.created_at ? new Date(row.created_at).toLocaleString("es-MX") : "";
        const number = String(index + 1).padStart(2, "0");
        return '<li><span class="idx">' + number + "</span>" +
          '<div><span class="name">' + escapeHtml(row.label) + "</span>" +
          "<time>" + escapeHtml(when) + "</time></div>" +
          '<span class="pct">' + pct + "%</span></li>";
      }).join("");
    } catch (err) {
      list.innerHTML = '<li class="placeholder-row">No se pudo cargar el registro.</li>';
    }
  }

  async function checkHealth() {
    const badge = $("netBadge");
    try {
      const response = await fetch(apiBase() + "/health");
      if (!response.ok) throw new Error("HTTP " + response.status);
      const health = await response.json();
      if (health.status === "ok") {
        badge.textContent = health.model_loaded ? "API y modelo listos" : "API lista · modelo cargando";
        badge.className = "status ok";
      } else {
        badge.textContent = "API degradada";
        badge.className = "status warn";
      }
    } catch (err) {
      badge.textContent = "Sin conexión";
      badge.className = "status err";
    }
  }

  $("btnCamera").addEventListener("click", startCamera);
  $("btnCapture").addEventListener("click", capture);
  $("btnRecognize").addEventListener("click", recognize);
  $("btnRefresh").addEventListener("click", () => {
    checkHealth();
    loadHistory();
  });

  $("fileInput").addEventListener("change", (event) => {
    const file = event.target.files && event.target.files[0];
    if (file) setBlob(file, file.name);
  });

  $("apiBase").value = DEFAULT_API;
  $("apiBase").addEventListener("change", () => {
    localStorage.setItem("paakat_api", $("apiBase").value.trim());
    checkHealth();
    loadHistory();
  });

  checkHealth();
  loadHistory();
})();
