function toggleChat() {
  document.getElementById('chatbot-window').classList.toggle('open');
}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

function appendMessage(text, sender) {
  const body = document.getElementById('chatbot-body');
  const div = document.createElement('div');
  div.className = 'chat-msg ' + sender;
  div.textContent = text;
  body.appendChild(div);
  body.scrollTop = body.scrollHeight;
}

async function sendChatMessage(event) {
  event.preventDefault();
  const input = document.getElementById('chatbot-text');
  const message = input.value.trim();
  if (!message) return;
  appendMessage(message, 'user');
  input.value = '';

  try {
    const res = await fetch('/api/chatbot/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({ message }),
    });
    const data = await res.json();
    appendMessage(data.response || "Sorry, I couldn't process that.", 'bot');
  } catch (err) {
    appendMessage("Network error. Please try again.", 'bot');
  }
}
