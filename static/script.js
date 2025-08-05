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
    const data = await res.json();

    typing.remove();
    appendMessage("jarvis", data.answer || "Sorry, I couldn't understand that.");

    if (ttsToggle.checked && "speechSynthesis" in window) {
      const utter = new SpeechSynthesisUtterance(data.answer);
      window.speechSynthesis.speak(utter);
    }
  } catch (e) {
    typing.remove();
    appendMessage("jarvis", "Error talking to the server.");
    console.error(e);
  }
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const q = input.value.trim();
  if (!q) return;
  input.value = "";
  ask(q);
});

document.getElementById('voiceBtn').addEventListener('click', function () {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-IN';  // or 'en-US'
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.start();

    recognition.onresult = function (event) {
        const transcript = event.results[0][0].transcript;
        document.getElementById('userInput').value = transcript;
    };

    recognition.onerror = function (event) {
        console.error('Speech recognition error', event.error);
    };
});

function askQuestion() {
      const question = document.getElementById("question").value;
      fetch('/ask', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ question: question })
      })
      .then(res => res.json())
      .then(data => {
        document.getElementById("response").textContent = data.answer;
        speakAnswer(data.answer); // speak output
      });
    }

    function startListening() {
      if (!('webkitSpeechRecognition' in window)) {
        alert("Your browser doesn't support speech recognition.");
        return;
      }

      const recognition = new webkitSpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'en-IN';

      recognition.start();

      recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        document.getElementById("question").value = transcript;
        askQuestion();
      };

      recognition.onerror = function(event) {
        alert("Speech recognition error: " + event.error);
      };
    }

    function speakAnswer(text) {
      const synth = window.speechSynthesis;
      const utter = new SpeechSynthesisUtterance(text);
      utter.lang = 'en-IN';
      synth.speak(utter);
    }

document.getElementById("chat-form").addEventListener("submit", function (e) {
  e.preventDefault();

  const input = document.getElementById("query");
  const mode = document.getElementById("mode").value;
  const userQuery = input.value.trim();
  input.value = "";

  if (!userQuery) return;

  // Append user's question to the chat
  const chat = document.getElementById("chat");
  const userDiv = document.createElement("div");
  userDiv.className = "user-msg";
  userDiv.textContent = userQuery;
  chat.appendChild(userDiv);

  fetch("/ask", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ query: userQuery, mode: mode })
  })
    .then(res => res.json())
    .then(data => {
      const botDiv = document.createElement("div");
      botDiv.className = "bot-msg";
      botDiv.textContent = data.answer;
      chat.appendChild(botDiv);

      // Text-to-Speech
      if (document.getElementById("ttsToggle").checked) {
        const utterance = new SpeechSynthesisUtterance(data.answer);
        speechSynthesis.speak(utterance);
      }
    })
    .catch(error => console.error("Error:", error));
});

// ✅ Reusable ask function (fixed)
async function ask(query, mode = "school") {
  appendMessage("user", query);

  const typing = document.createElement("div");
  typing.className = "msg jarvis typing";
  typing.innerHTML = `<span class="who">GYAN</span><p>...</p>`;
  chat.appendChild(typing);
  chat.scrollTop = chat.scrollHeight;

  try {
    const res = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, mode })
    });

    const data = await res.json();
    typing.remove();
    appendMessage("jarvis", data.answer || "Sorry, I couldn't understand that.");

    if (ttsToggle.checked && "speechSynthesis" in window) {
      const utter = new SpeechSynthesisUtterance(data.answer);
      window.speechSynthesis.speak(utter);
    }
  } catch (e) {
    typing.remove();
    appendMessage("jarvis", "Error talking to the server.");
    console.error(e);
  }
}

// ✅ Use selected mode on form submit
document.getElementById("chat-form").addEventListener("submit", function (e) {
  e.preventDefault();

  const query = input.value.trim();
  const mode = document.getElementById("mode").value; // 🧠 get selected mode
  input.value = "";

  if (!query) return;
  ask(query, mode);
});

// 🎤 Voice input trigger (make sure it calls ask(query, mode))
document.getElementById('voiceBtn')?.addEventListener('click', function () {
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  recognition.lang = 'en-IN';
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.start();

  recognition.onresult = function (event) {
    const transcript = event.results[0][0].transcript;
    const mode = document.getElementById("mode").value;
    ask(transcript, mode); // ✅ pass mode from dropdown
  };

  recognition.onerror = function (event) {
    console.error('Speech recognition error', event.error);
  };
});
botDiv.innerHTML = data.answer.replace(/\n/g, "<br>");
