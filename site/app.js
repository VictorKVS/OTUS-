const REPO = "https://github.com/VictorKVS/OTUS-";
const BRANCH = "feature/otus-homework-site";

const lessons = [
  [1,"Пресейл, контракты и работа с требованиями","materials","BUS · REQ · границы проекта","1. Пресейл, контракты и работа с требованиями закладываем фундамент проекта"],
  [2,"Проектирование и оценка: план, риски и смета","materials","RISK · COST · планирование","2. Проектирование и оценка от требований к плану, рискам и смете"],
  [3,"Стратегия поставки ценности: PoC → Production","materials","Value · roadmap · delivery","3. Стратегия поставки ценности от PoC до Production  ДЗ"],
  [4,"Высокоуровневое проектирование с C4","materials","HLD · C4 · контексты","4. Высокоуровневое проектирование (HLD) с использованием C4 Model"],
  [5,"LLD: компоненты и взаимодействия","done","C3 · OpenAPI · Sequence · BPMN · DFD","5. Низкоуровневое проектирование (LLD) компоненты и взаимодействия  ДЗ"],
  [6,"Архитектурные паттерны RAG","materials","Retrieval · embeddings · Vector DB","6. Архитектурные паттерны RAG и его продвинутые вариации"],
  [7,"AI-агенты и Multi-Agent Systems","done","LangGraph · Hybrid RAG · handoffs","7. Архитектурные паттерны AI-агенты и Multi-Agent Systems  ДЗ"],
  [8,"Architecture Decision Records","lab","ADR · lifecycle · supersede","8. Документирование решений Architecture Decision Records (ADR)"],
  [9,"Верификация архитектуры и CTO Challenge","review","ATAM · ADR · TCO · pitch","9. Верификация архитектуры и CTO Challenge  ДЗ"],
  [10,"Архитектурный надзор и технический долг","materials","Governance · review · debt","10 .Архитектурный надзор и управление техническим долгом"],
  [11,"Интеграции: классика и AI-стандарты","materials","API · Broker · A2A · MCP","11 Проектирование интеграций от классики до AI-стандартов"],
  [12,"Архитектура данных для AI-систем","draft","Stream/Batch · Lake · Feature Store · Vector DB","12.  Архитектура данных для AI-систем  ДЗ"],
  [13,"Оценка качества и тестирование GenAI","lab","RAGAS · MLflow · Langfuse · CI","13 . Оценка качества и тестирование GenAI-компонентов"],
  [14,"Security by Design для AI-систем","materials","Threats · controls · secure architecture","14. Security by Design архитектура для защиты AI-систем"],
  [15,"Observability","materials","Metrics · traces · logs · SLO","15.Архитектура наблюдаемости (Observability)  ДЗ"],
  [16,"Sizing приложений и данных","materials","Capacity · load · resources","16. Расчёт ресурсов (Sizing) для приложений и данных"],
  [17,"Sizing и оптимизация инференса LLM","materials","GPU · VRAM · throughput · batching","17. Расчёт ресурсов и оптимизация инференса LLM  ДЗ"],
  [18,"Infrastructure as Code и CI/CD","materials","IaC · pipelines · environments","18 Инфраструктура как код (IaC) и CICD"],
  [19,"Архитектура MLOps-конвейеров","materials","Model lifecycle · registry · automation","19. Архитектура MLOps-конвейеров"],
  [20,"Стратегии развёртывания и Production","materials","Canary · rollback · deployment","20 Стратегии развёртывания и вывода в Production  ДЗ"],
  [21,"Высокая доступность и Disaster Recovery","materials","HA · DR · RTO · RPO","21. Архитектура высокой доступности (HA) и восстановления (DR)"],
  [22,"Serverless vs Kubernetes для AI","materials","Workload placement · orchestration","22 . Serverless vs. Kubernetes для AI-ворклоадов"],
  [23,"Событийно-ориентированная архитектура","materials","EDA · events · broker · consistency","23. Событийно-ориентированная архитектура (EDA) для AI"],
  [24,"High-Load и Low-Latency inference","materials","Scale · p95 · caching · queues","24. Архитектура для High-Load и Low-Latency инференса  ДЗ"],
  [25,"Гибридная и мультиоблачная архитектура","materials","Hybrid · multi-cloud · portability","25. Гибридная и мультиоблачная архитектура для AI"],
  [26,"Multi-tenancy в AI SaaS","materials","Isolation · quotas · tenant data","26. Архитектура для Multi-tenancy в AI SaaS"],
  [27,"Federated Learning и Privacy-Preserving","materials","Privacy · federation · locality","27. Federated Learning и Privacy-Preserving архитектура"],
  [28,"FinOps: архитектура, управляемая стоимостью","materials","Unit economics · TCO · budgets","28. FinOps архитектура, управляемая стоимостью"],
  [29,"Технологический радар и эволюция архитектуры","materials","Radar · lifecycle · adoption","29. Технологический радар и эволюция архитектуры"],
  [30,"Ethical AI by Design и Governance","materials","Governance · Model Card · accountability","30. Ethical AI by Design и архитектура для Governance  ДЗ"],
  [31,"API как продукт","materials","API product · lifecycle · governance","31. API как продукт проектирование и управление"]
].map(([id,title,status,evidence,path])=>({id,title,status,evidence,path}));

const gates = [
  {id:"G1",range:[1,3],title:"Замысел и ценность",result:"Vision, требования, риски, смета, поставка"},
  {id:"G2",range:[4,7],title:"Проектирование решения",result:"C4, LLD, RAG и Agent design"},
  {id:"G3",range:[8,10],title:"Решения и контроль",result:"ADR, CTO review, technical debt"},
  {id:"G4",range:[11,15],title:"Данные, качество и безопасность",result:"Integration, Data, Quality, Security, Observability"},
  {id:"G5",range:[16,20],title:"Промышленная поставка",result:"Sizing, IaC, MLOps, CI/CD, Deployment"},
  {id:"G6",range:[21,27],title:"Надёжность и масштаб",result:"HA/DR, K8s, EDA, High-load, Cloud, Privacy"},
  {id:"G7",range:[28,31],title:"Экономика и управление",result:"FinOps, Radar, Governance, API Product"}
];

const labels = {done:"ГОТОВО",review:"REVIEW",draft:"DRAFT",lab:"LAB",materials:"МАТЕРИАЛЫ"};
const evidenceStatuses = new Set(["done","review","draft","lab"]);
const chain = ["BUS","REQ/NFR","RISK","ADR","CMP","CTRL","TEST","SLO","COST","REL"];

function repoUrl(path){return `${REPO}/tree/${BRANCH}/${path.split('/').map(encodeURIComponent).join('/')}`;}
function renderChain(target){target.innerHTML=chain.map(x=>`<span>${x}</span>`).join("");}

function renderStats(){
  const counts = Object.fromEntries(Object.keys(labels).map(k=>[k,lessons.filter(x=>x.status===k).length]));
  const cards = [
    [31,"уроков"],[7,"контрольных gates"],[counts.done,"подтверждено готовыми"],[counts.review+counts.draft,"в review / draft"],[counts.lab,"рабочих lab-контуров"]
  ];
  document.querySelector('#stats').innerHTML = cards.map(([n,t])=>`<div class="stat"><b>${n}</b><span>${t}</span></div>`).join('');
}

function renderGates(){
  document.querySelector('#gateGrid').innerHTML = gates.map(g=>{
    const group=lessons.filter(l=>l.id>=g.range[0]&&l.id<=g.range[1]);
    const evidenced=group.filter(l=>evidenceStatuses.has(l.status)).length;
    const pct=Math.round(evidenced/group.length*100);
    return `<article class="gate"><div class="gate-head"><span>${g.id}</span><span>${g.range[0]}–${g.range[1]}</span></div><h3>${g.title}</h3><p>${g.result}</p><div class="progress" title="Уроки с подтверждённым артефактом: ${evidenced}/${group.length}"><i style="width:${pct}%"></i></div></article>`;
  }).join('');
}

function renderLessons(){
  const q=document.querySelector('#lessonSearch').value.trim().toLowerCase();
  const status=document.querySelector('#statusFilter').value;
  const filtered=lessons.filter(l=>(status==='all'||l.status===status)&&(!q||`${l.title} ${l.evidence}`.toLowerCase().includes(q)));
  document.querySelector('#lessonGrid').innerHTML = filtered.length ? filtered.map(l=>`
    <article class="lesson-card">
      <div class="lesson-top"><span class="lesson-no">LESSON ${String(l.id).padStart(2,'0')}</span><span class="badge ${l.status}">${labels[l.status]}</span></div>
      <h3>${l.title}</h3><p>${l.evidence}</p>
      <a href="${repoUrl(l.path)}" target="_blank" rel="noopener">Артефакты урока ↗</a>
    </article>`).join('') : `<div class="empty">По выбранным условиям уроков не найдено.</div>`;
}

function initLinks(){document.querySelectorAll('[data-repo-path]').forEach(a=>a.href=`${REPO}/blob/${BRANCH}/${a.dataset.repoPath.split('/').map(encodeURIComponent).join('/')}`);}
function initTheme(){
  const root=document.documentElement;
  const saved=localStorage.getItem('otus-theme');
  if(saved) root.dataset.theme=saved;
  document.querySelector('#themeToggle').addEventListener('click',()=>{
    const next=root.dataset.theme==='light'?'dark':'light';
    root.dataset.theme=next;localStorage.setItem('otus-theme',next);
  });
}

renderChain(document.querySelector('#heroChain'));
renderChain(document.querySelector('#traceChain'));
renderStats();renderGates();renderLessons();initLinks();initTheme();
document.querySelector('#lessonSearch').addEventListener('input',renderLessons);
document.querySelector('#statusFilter').addEventListener('change',renderLessons);
