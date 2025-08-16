const chat = document.getElementById("chat");
const form = document.getElementById("chat-form");
const input = document.getElementById("query");
const ttsToggle = document.getElementById("ttsToggle");

function appendMessage(who, text) {
  const div = document.createElement("div");
  div.className = `msg ${who}`;
  div.innerHTML = `<span class="who">${who === "user" ? "You" : "GYAN"}</span><p>${text}</p>`;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

async function ask(query) {
  appendMessage("user", query);

  // Show typing indicator
  const typing = document.createElement("div");
  typing.className = "msg jarvis typing";
  typing.innerHTML = `<span class="who">GYAN</span><p>...</p>`;
  chat.appendChild(typing);
  chat.scrollTop = chat.scrollHeight;

  try {
    const res = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });
    
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    
    const data = await res.json();

    typing.remove();
    appendMessage("jarvis", data.answer || "Sorry, I couldn't understand that.");

    if (ttsToggle.checked && "speechSynthesis" in window) {
      const utter = new SpeechSynthesisUtterance(data.answer);
      window.speechSynthesis.speak(utter);
    }
  } catch (e) {
    typing.remove();
    appendMessage("jarvis", "Error talking to the server. Please check if the server is running.");
    console.error("Error details:", e);
  }
}

// Main form submission
form.addEventListener("submit", (e) => {
  e.preventDefault();
  const q = input.value.trim();
  if (!q) return;
  input.value = "";
  ask(q);
});

// Voice input functionality
document.getElementById('voiceBtn')?.addEventListener('click', function () {
  if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
    alert("Your browser doesn't support speech recognition.");
    return;
  }

  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  recognition.lang = 'en-IN';
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.start();

  recognition.onresult = function (event) {
    const transcript = event.results[0][0].transcript;
    input.value = transcript;
    ask(transcript);
  };

  recognition.onerror = function (event) {
    console.error('Speech recognition error', event.error);
    alert("Speech recognition error: " + event.error);
  };
});
