(function () {
  const { $ } = window.Paakat;

  const GROQ_KEY = (window.PAAKAT_CONFIG && window.PAAKAT_CONFIG.GROQ_KEY) || "";
  const GROQ_URL = "https://api.groq.com/openai/v1/chat/completions";
  const GROQ_MODEL = "openai/gpt-oss-120b";

  const SYSTEM_PROMPT =
    "Eres la guía turística virtual de Paakat, una app que identifica monumentos arqueológicos del patrimonio indígena de México a partir de una foto. Responde en español, con tono cercano, claro y breve (máximo 120 palabras). Da datos verificables sobre culturas y sitios arqueológicos de México (maya, mexica/azteca, zapoteca, mixteca, olmeca, teotihuacana, totonaca, purépecha, entre otras). Si no estás seguro de un dato, dilo; no inventes ubicaciones ni fechas. Si la pregunta no trata de turismo o patrimonio cultural, redirige amablemente la conversación.";

  const chatHistory = [{ role: "system", content: SYSTEM_PROMPT }];
  let chatBusy = false;

  function appendChat(role, text) {
    const log = $("chatLog");
    const msg = document.createElement("div");
    msg.className = "chat-msg " + (role === "user" ? "user" : "bot");
    msg.textContent = text;
    log.appendChild(msg);
    log.scrollTop = log.scrollHeight;
    return msg;
  }

  function setChatOpen(open) {
    $("chatPanel").hidden = !open;
    $("chatToggle").setAttribute("aria-expanded", open ? "true" : "false");
    if (open) $("chatInput").focus();
  }

  async function sendChat(message) {
    if (chatBusy || !message) return;
    if (!GROQ_KEY) {
      appendChat("bot", "Falta configurar la API key. Crea web/js/config.js a partir de config.example.js.");
      return;
    }
    chatBusy = true;
    $("chatSend").disabled = true;
    $("chatInput").disabled = true;
    appendChat("user", message);
    chatHistory.push({ role: "user", content: message });
    while (chatHistory.length > 21) chatHistory.splice(1, 1);

    const typing = appendChat("bot", "Pensando…");
    typing.classList.add("typing");

    try {
      const response = await fetch(GROQ_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + GROQ_KEY
        },
        body: JSON.stringify({
          model: GROQ_MODEL,
          messages: chatHistory,
          temperature: 0.6,
          max_tokens: 600
        })
      });
      if (!response.ok) {
        const detail = await response.text();
        throw new Error("HTTP " + response.status + " · " + detail.slice(0, 160));
      }
      const data = await response.json();
      const reply = (
        data.choices && data.choices[0] && data.choices[0].message
          ? data.choices[0].message.content
          : ""
      ).trim();
      typing.classList.remove("typing");
      typing.textContent = reply || "No obtuve respuesta. Intenta de nuevo.";
      if (reply) chatHistory.push({ role: "assistant", content: reply });
    } catch (err) {
      typing.classList.remove("typing");
      typing.textContent = "Error al consultar la guía: " + err.message;
    } finally {
      chatBusy = false;
      $("chatSend").disabled = false;
      $("chatInput").disabled = false;
      $("chatInput").focus();
      $("chatLog").scrollTop = $("chatLog").scrollHeight;
    }
  }

  $("chatToggle").addEventListener("click", () => setChatOpen($("chatPanel").hidden));
  $("chatClose").addEventListener("click", () => setChatOpen(false));
  $("chatForm").addEventListener("submit", (event) => {
    event.preventDefault();
    const input = $("chatInput");
    const message = input.value.trim();
    if (!message) return;
    input.value = "";
    sendChat(message);
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !$("chatPanel").hidden) setChatOpen(false);
  });
})();
