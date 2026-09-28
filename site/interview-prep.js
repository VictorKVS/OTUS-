
const STORAGE_KEY='otus-interview-prep-state-v1';
const state=JSON.parse(localStorage.getItem(STORAGE_KEY)||'{}');
let tracks=[];
const labels={learn:'LEARN',practice:'PRACTICE',ready:'READY'};
const order=['learn','practice','ready'];

function getState(id){return state[id]||'learn'}
function setState(id,value){state[id]=value;localStorage.setItem(STORAGE_KEY,JSON.stringify(state));render();}
function nextState(id){const cur=getState(id);setState(id,order[(order.indexOf(cur)+1)%order.length]);}

function renderProgress(){
  const ready=tracks.filter(t=>getState(t.id)==='ready').length;
  document.querySelector('#readyCount').textContent=ready;
  document.querySelector('#totalCount').textContent=tracks.length;
  document.querySelector('#totalProgress').style.width=(tracks.length?Math.round(ready/tracks.length*100):0)+'%';
}
function render(){
  const q=document.querySelector('#trackSearch').value.trim().toLowerCase();
  const f=document.querySelector('#trackFilter').value;
  const filtered=tracks.filter(t=>(f==='all'||getState(t.id)===f)&&(!q||(t.title+' '+t.topics.join(' ')).toLowerCase().includes(q)));
  document.querySelector('#trackGrid').innerHTML=filtered.map(t=>`
    <article class="prep-card">
      <div class="prep-meta"><span class="prep-level">${t.level}</span><span class="badge ${getState(t.id)==='ready'?'done':getState(t.id)==='practice'?'review':'materials'}">${labels[getState(t.id)]}</span></div>
      <h3>${t.title}</h3>
      <div class="prep-topics">${t.topics.map(x=>`<span>${x}</span>`).join('')}</div>
      <ol>${t.questions.map(x=>`<li>${x}</li>`).join('')}</ol>
      <div class="prep-actions"><a href="${t.doc}">Playbook →</a><button class="state-btn" data-state="${getState(t.id)}" data-id="${t.id}">Следующий статус</button></div>
    </article>`).join('') || '<div class="empty">Ничего не найдено.</div>';
  document.querySelectorAll('.state-btn').forEach(b=>b.addEventListener('click',()=>nextState(b.dataset.id)));
  renderProgress();
}
function initTheme(){
  const root=document.documentElement;
  const saved=localStorage.getItem('otus-theme'); if(saved)root.dataset.theme=saved;
  document.querySelector('#themeToggle').addEventListener('click',()=>{const next=root.dataset.theme==='light'?'dark':'light';root.dataset.theme=next;localStorage.setItem('otus-theme',next);});
}
async function init(){
  const r=await fetch('./data/interview-prep.json',{cache:'no-store'});
  const data=await r.json(); tracks=data.tracks||[];
  document.querySelector('#prepChain').innerHTML=(data.method||'').split('→').map(x=>`<span>${x.trim()}</span>`).join('');
  render();
}
document.querySelector('#trackSearch').addEventListener('input',render);
document.querySelector('#trackFilter').addEventListener('change',render);
initTheme(); init();
