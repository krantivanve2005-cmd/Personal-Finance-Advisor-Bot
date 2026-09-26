function toggleSidebar(){
  document.getElementById('sidebar').classList.toggle('open');
}

function openModal(id){ document.getElementById(id).classList.add('open'); }
function closeModal(id){ document.getElementById(id).classList.remove('open'); }

const AI_ASK_URL = window.AI_ASK_URL || '/api/advisor/ask';
const CSRF_TOKEN = window.CSRF_TOKEN || '';

function appendMsg(text, cls){
  const log = document.getElementById('chat-log');
  if(!log) return;
  const d = document.createElement('div');
  d.className = 'msg ' + cls;
  d.textContent = text;
  log.appendChild(d);
  log.scrollTop = log.scrollHeight;
}

async function sendChat(){
  const input = document.getElementById('chat-text');
  const val = input.value.trim();
  if(!val) return;
  appendMsg(val, 'user');
  input.value = '';
  appendMsg('Thinking…', 'ai typing');

  try{
    const res = await fetch(AI_ASK_URL, {
      method: 'POST',
      headers: {'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN},
      body: JSON.stringify({prompt: val})
    });
    const data = await res.json();
    document.querySelector('.msg.typing')?.remove();
    appendMsg(data.response || data.error || 'Something went wrong.', 'ai');
  }catch(err){
    document.querySelector('.msg.typing')?.remove();
    appendMsg('Could not reach the AI Advisor service. Please try again.', 'ai');
  }
}

function chip(btn){
  const input = document.getElementById('chat-text');
  if(!input) return;
  input.value = btn.textContent;
  sendChat();
}

document.addEventListener('DOMContentLoaded', () => {
  const chatInput = document.getElementById('chat-text');
  if(chatInput){
    chatInput.addEventListener('keydown', e => { if(e.key === 'Enter') sendChat(); });
  }
  document.querySelectorAll('.flash').forEach(f => {
    setTimeout(() => f.remove(), 5000);
  });
});
