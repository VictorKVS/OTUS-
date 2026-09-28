let items=[];
function esc(s){return String(s)}
function render(){
 const q=document.querySelector('#stackSearch').value.trim().toLowerCase();
 const f=document.querySelector('#kindFilter').value;
 const shown=items.filter(x=>(f==='all'||x.kind===f)&&(!q||(x.name+' '+x.kind+' '+x.short+' '+x.father.join(' ')).toLowerCase().includes(q)));
 document.querySelector('#countTitle').textContent=shown.length+' capability';
 document.querySelector('#stackGrid').innerHTML=shown.map(x=>`
 <article class="stack-card">
   <div class="stack-kind">${esc(x.kind)} · ${esc(x.level)}</div>
   <h3>${esc(x.name)}</h3>
   <p>${esc(x.short)}</p>
   <div class="stack-flow">${esc(x.flow)}</div>
   <p><b>Зачем:</b> ${esc(x.purpose)}</p>
   <div class="stack-tags">${x.father.map(t=>'<span>'+esc(t)+'</span>').join('')}</div>
   <p><b>Риски:</b> ${x.risks.map(esc).join(' · ')}</p>
   <p class="stack-q"><b>Собеседование:</b> ${esc(x.interview)}</p>
 </article>`).join('');
}
function initTheme(){const root=document.documentElement;const saved=localStorage.getItem('otus-theme');if(saved)root.dataset.theme=saved;document.querySelector('#themeToggle').addEventListener('click',()=>{const next=root.dataset.theme==='light'?'dark':'light';root.dataset.theme=next;localStorage.setItem('otus-theme',next);});}
fetch('./data/ai-capability-stack-2026.json',{cache:'no-store'}).then(r=>r.json()).then(d=>{
 items=d.items||[];
 const kinds=[...new Set(items.map(x=>x.kind))].sort();
 document.querySelector('#kindFilter').innerHTML='<option value="all">Все типы</option>'+kinds.map(k=>'<option value="'+k+'">'+k+'</option>').join('');
 render();
});
document.querySelector('#stackSearch').addEventListener('input',render);
document.querySelector('#kindFilter').addEventListener('change',render);
initTheme();