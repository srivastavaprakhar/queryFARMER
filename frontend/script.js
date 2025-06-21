let token = null;

function toggleSignup() {
  document.getElementById("login-container").classList.add("hidden");
  document.getElementById("signup-container").classList.remove("hidden");
}

function toggleLogin() {
  document.getElementById("signup-container").classList.add("hidden");
  document.getElementById("login-container").classList.remove("hidden");
}

async function handleLogin() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  try {
    const response = await fetch("http://127.0.0.1:8000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });

    if (!response.ok) throw new Error("Login failed");

    token = (await response.json()).token;
    document.getElementById("login-container").classList.add("hidden");
    document.getElementById("chat-container").classList.remove("hidden");
  } catch (err) {
    alert("Login failed: " + err.message);
  }
}

async function handleSignup() {
  const username = document.getElementById("new-username").value;
  const password = document.getElementById("new-password").value;

  try {
    const response = await fetch("http://127.0.0.1:8000/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });

    if (!response.ok) throw new Error("Signup failed");

    alert("Signup successful! Please log in.");
    toggleLogin();
  } catch (err) {
    alert("Signup failed: " + err.message);
  }
}

async function askQuestion() {
  const input = document.getElementById("question");
  const question = input.value.trim();
  const chatBox = document.getElementById("chat-box");

  if (!question) return;

  // Add user message
  addMessage("user", question);
  input.value = "";

  // Add temporary bot "thinking..." message
  const thinkingMsg = addMessage("bot", "Thinking... 🤔", true);

  try {
    const response = await fetch("http://127.0.0.1:8000/ask", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ question })
    });

    const data = await response.json();

    // Replace thinking message with actual response
    thinkingMsg.innerText = data.answer || "No answer.";
  } catch (err) {
    thinkingMsg.innerText = "Error contacting the server.";
    console.error(err);
  }
}

function addMessage(sender, text, returnNode = false) {
  const chatBox = document.getElementById("chat-box");
  const message = document.createElement("div");
  message.className = `message ${sender}`;
  message.innerText = text;
  chatBox.appendChild(message);
  chatBox.scrollTop = chatBox.scrollHeight;

  return returnNode ? message : null;
}
