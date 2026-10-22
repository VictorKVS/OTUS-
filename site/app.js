const REPO = "https://github.com/VictorKVS/OTUS-";
const BRANCH = "feature/otus-homework-site";

let lessons = [];
let gates = [];

const labels = {done:"ГОТОВО",review:"REVIEW",draft:"DRAFT",lab:"LAB",materials:"МАТЕРИАЛЫ"};
const evidenceStatuses = new Set(["done","review","draft","lab"]);
const chain = ["BUS","REQ/NFR","RISK","ADR","CMP","CTRL","TEST","SLO","COST","REL"];

function repoUrl(path){return `${REPO}/tree/${BRANCH}/${path.split('/').map(encodeURIComponent).join('/')}`;}
function renderChain(target){target.innerHTML=chain.map(x=>`<span>${x}</span>`).join("");}

function renderStats(){
  const counts = Object.fromEntries(Object.keys(labels).map(k=>[k,lessons.filter(x=>x.status===k).length]));
  const cards = [[lessons.length,"уроков"],[gates.length,"контрольных gates"],[counts.done||0,"подтверждено готовыми"],[(counts.review||0)+(counts.draft||0),"в review / draft"],[counts.lab||0,"рабочих lab-контуров"]];
  document.querySelector('#stats').innerHTML = cards.map(([n,t])=>`<div class="stat"><b>${n}</b><span>${t}</span></div>`).join('');
}

function renderGates(){
  document.querySelector('#gateGrid').innerHTML = gates.map(g=>{
    const group=lessons.filter(l=>l.id>=g.range[0]&&l.id<=g.range[1]);
    const evidenced=group.filter(l=>evidenceStatuses.has(l.status)).length;
    const pct=group.length?Math.round(evidenced/group.length*100):0;
    return `<article class="gate"><div class="gate-head"><span>${g.id}</span><span>${g.range[0]}–${g.range[1]}</span></div><h3>${g.title}</h3><p>${g.result}</p><div class="progress" title="Уроки с подтверждённым артефактом: ${evidenced}/${group.length}"><i style="width:${pct}%"></i></div></article>`;
  }).join('');
}

function renderLessons(){
  const q=document.querySelector('#lessonSearch').value.trim().toLowerCase();
  const status=document.querySelector('#statusFilter').value;
  const filtered=lessons.filter(l=>(status==='all'||l.status===status)&&(!q||`${l.title} ${l.evidence}`.toLowerCase().includes(q)));
  document.querySelector('#lessonGrid').innerHTML = filtered.length ? filtered.map(l=>{
    const expert=l.expertPath?`<a class="expert-link" href="${l.expertPath}">Эксперт-разбор →</a>`:'';
    const maturity=l.maturity?`<span class="badge draft">${l.maturity}</span>`:'';
    return `<article class="lesson-card"><div class="lesson-top"><span class="lesson-no">LESSON ${String(l.id).padStart(2,'0')}</span><span><span class="badge ${l.status}">${labels[l.status]}</span> ${maturity}</span></div><h3>${l.title}</h3><p>${l.evidence}</p><div class="lesson-links">${expert}<a href="${repoUrl(l.path)}" target="_blank" rel="noopener">Артефакты ↗</a></div></article>`;
  }).join('') : `<div class="empty">По выбранным условиям уроков не найдено.</div>`;
}

function initLinks(){document.querySelectorAll('[data-repo-path]').forEach(a=>a.href=`${REPO}/blob/${BRANCH}/${a.dataset.repoPath.split('/').map(encodeURIComponent).join('/')}`);}
function initTheme(){const root=document.documentElement;const saved=localStorage.getItem('otus-theme');if(saved)root.dataset.theme=saved;document.querySelector('#themeToggle').addEventListener('click',()=>{const next=root.dataset.theme==='light'?'dark':'light';root.dataset.theme=next;localStorage.setItem('otus-theme',next);});}

async function initCourse(){
  try{
    const response=await fetch('./data/course-manifest.json',{cache:'no-store'});
    if(!response.ok) throw new Error(`HTTP ${response.status}`);
    const data=await response.json();
    lessons=data.lessons||[];
    gates=data.gates||[];
    renderStats();renderGates();renderLessons();
  }catch(error){
    document.querySelector('#stats').innerHTML=`<div class="empty">Не удалось загрузить course manifest: ${error.message}. Запускайте сайт через HTTP server.</div>`;
    document.querySelector('#lessonGrid').innerHTML=`<div class="empty">Course manifest unavailable.</div>`;
  }
}

renderChain(document.querySelector('#heroChain'));
renderChain(document.querySelector('#traceChain'));
initLinks();initTheme();
document.querySelector('#lessonSearch').addEventListener('input',renderLessons);
document.querySelector('#statusFilter').addEventListener('change',renderLessons);
initCourse();


function escField(v){return String(v??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}

function renderFieldBranch(field, branchId){
  const branch=field.branches.find(x=>x.id===branchId)||field.branches[0];
  document.querySelectorAll('.field-tab').forEach(btn=>btn.classList.toggle('active',btn.dataset.branch===branch.id));
  const feeds=(branch.feeds||[]).map(id=>{
    const target=field.branches.find(x=>x.id===id);
    return target?target.tab:id;
  });
  document.querySelector('#fieldWorkspace').innerHTML=
    '<div class="field-branch-head"><div><div class="eyebrow">'+escField(branch.agent_family)+' · '+escField(branch.overlay)+'</div><h3>'+escField(branch.tab)+'</h3><p>'+escField(branch.role)+'</p></div><span class="branch-status">'+escField(branch.status)+'</span></div>'+
    '<div class="field-branch-grid">'+
      '<div class="branch-box"><b>INPUT</b>'+(branch.input||[]).map(x=>'<span>'+escField(x)+'</span>').join('')+'</div>'+
      '<div class="branch-box"><b>PROCESSING LAYER</b><span>FATHER Analytical Core</span><span>'+escField(branch.overlay)+'</span><span>optional K2</span></div>'+
      '<div class="branch-box"><b>OUTPUT</b>'+(branch.output||[]).map(x=>'<span>'+escField(x)+'</span>').join('')+'</div>'+
    '</div>'+
    '<div class="branch-flow"><strong>Связи:</strong> '+escField(branch.tab)+' → '+feeds.map(escField).join(' · ')+'<br><strong>Контракт:</strong> COMMON BASE + K1 OVERLAY + OPTIONAL K2 → TESTS → EVIDENCE → RETURN TO ANALYTICS</div>';
}

async function initFatherField(){
  const host=document.querySelector('#fieldTabs');
  if(!host) return;
  try{
    const r=await fetch('./data/father-field.json',{cache:'no-store'});
    if(!r.ok) throw new Error('HTTP '+r.status);
    const field=await r.json();
    document.querySelector('#fieldFoundation').innerHTML=(field.shared_foundation||[]).map(x=>'<div class="foundation-cell"><b>'+escField(x.name)+'</b><small>'+escField(x.purpose)+'</small></div>').join('');
    host.innerHTML=(field.branches||[]).map((x,i)=>'<button class="field-tab '+(i===0?'active':'')+'" data-branch="'+escField(x.id)+'">'+escField(x.tab)+(x.status==='PLANNED'?'<em>PLANNED</em>':'')+'</button>').join('');
    host.querySelectorAll('.field-tab').forEach(btn=>btn.addEventListener('click',()=>renderFieldBranch(field,btn.dataset.branch)));
    renderFieldBranch(field,'analytics');
  }catch(error){
    document.querySelector('#fieldWorkspace').innerHTML='<div class="empty">Не удалось загрузить FATHER Field: '+escField(error.message)+'</div>';
  }
}
initFatherField();
