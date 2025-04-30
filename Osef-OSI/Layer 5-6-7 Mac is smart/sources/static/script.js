const chatEl = document.getElementById('chat');

function render(msgs) {
  chatEl.innerHTML = msgs
    .map(m => `<li><strong>${m.author}:</strong> ${m.text}</li>`)
    .join('');
  chatEl.scrollTop = chatEl.scrollHeight;
}

async function ask() {
  await fetch('/post', { method: 'POST' });
}

document.getElementById('ask').addEventListener('click', ask);

// --- Live updates via Server-Sent Events --------------------------------
const evt = new EventSource('/stream');
evt.onmessage = e => render(JSON.parse(e.data));
