const chatEl = document.getElementById('chat');

function render(msgs){
  chatEl.innerHTML = msgs.map(m=>`<li><strong>${m.author}:</strong> ${m.text}</li>`).join('');
  chatEl.scrollTop = chatEl.scrollHeight;
}

async function loadChat(){
  const res = await fetch('/chat');
  render(await res.json());
}

async function ask(){
  await fetch('/post',{method:'POST'});
  await loadChat();
}

document.getElementById('ask').addEventListener('click', ask);
loadChat();
setInterval(loadChat, 3000);