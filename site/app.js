const REPO = "https://github.com/VictorKVS/OTUS-";
const BRANCH = "feature/otus-homework-site";

const lessons = [
  [1,"Пресейл, контракты и работа с требованиями","materials","BUS · REQ · границы проекта","1. Пресейл, контракты и работа с требованиями закладываем фундамент проекта","./lesson-01.html"],
  [2,"Проектирование и оценка: план, риски и смета","materials","RISK · COST · планирование","2. Проектирование и оценка от требований к плану, рискам и смете",null],
  [3,"Стратегия поставки ценности: PoC → Production","materials","Value · roadmap · delivery","3. Стратегия поставки ценности от PoC до Production  ДЗ",null],
  [4,"Высокоуровневое проектирование с C4","materials","HLD · C4 · контексты","4. Высокоуровневое проектирование (HLD) с использованием C4 Model",null],
  [5,"LLD: компоненты и взаимодействия","done","C3 · OpenAPI · Sequence · BPMN · DFD","5. Низкоуровневое проектирование (LLD) компоненты и взаимодействия  ДЗ",null],
  [6,"Архитектурные паттерны RAG","materials","Retrieval · embeddings · Vector DB","6. Архитектурные паттерны RAG и его продвинутые вариации",null],
  [7,"AI-агенты и Multi-Agent Systems","done","LangGraph · Hybrid RAG · handoffs","7. Архитектурные паттерны AI-агенты и Multi-Agent Systems  ДЗ",null],
  [8,"Architecture Decision Records","lab","ADR · lifecycle · supersede","8. Документирование решений Architecture Decision Records (ADR)",null],
  [9,"Верификация архитектуры и CTO Challenge","review","ATAM · ADR · TCO · pitch","9. Верификация архитектуры и CTO Challenge  ДЗ",null],
  [10,"Архитектурный надзор и технический долг","materials","Governance · review · debt","10 .Архитектурный надзор и управление техническим долгом",null],
  [11,"Интеграции: классика и AI-стандарты","materials","API · Broker · A2A · MCP","11 Проектирование интеграций от классики до AI-стандартов",null],
  [12,"Архитектура данных для AI-систем","draft","Stream/Batch · Lake · Feature Store · Vector DB","12.  Архитектура данных для AI-систем  ДЗ",null],
  [13,"Оценка качества и тестирование GenAI","lab","RAGAS · MLflow · Langfuse · CI","13 . Оценка качества и тестирование GenAI-компонентов",null],
  [14,"Security by Design для AI-систем","materials","Threats · controls · secure architecture","14. Security by Design архитектура для защиты AI-систем",null],
  [15,"Observability","materials","Metrics · traces · logs · SLO","15.Архитектура наблюдаемости (Observability)  ДЗ",null],
  [16,"Sizing приложений и данных","materials","Capacity · load · resources","16. Расчёт ресурсов (Sizing) для приложений и данных",null],
  [17,"Sizing и оптимизация инференса LLM","materials","GPU · VRAM · throughput · batching","17. Расчёт ресурсов и оптимизация инференса LLM  ДЗ",null],
  [18,"Infrastructure as Code и CI/CD","materials","IaC · pipelines · environments","18 Инфраструктура как код (IaC) и CICD",null],
  [19,"Архитектура MLOps-конвейеров","materials","Model lifecycle · registry · automation","19. Архитектура MLOps-конвейеров",null],
  [20,"Стратегии развёртывания и Production","materials","Canary · rollback · deployment","20 Стратегии развёртывания и вывода в Production  ДЗ",null],
  [21,"Высокая доступность и Disaster Recovery","materials","HA · DR · RTO · RPO","21. Архитектура высокой доступности (HA) и восстановления (DR)",null],
  [22,"Serverless vs Kubernetes для AI","materials","Workload placement · orchestration","22 . Serverless vs. Kubernetes для AI-ворклоадов",null],
  [23,"Событийно-ориентированная архитектура","materials","EDA · events · broker · consistency","23. Событийно-ориентированная архитектура (EDA) для AI",null],
  [24,"High-Load и Low-Latency inference","materials","Scale · p95 · caching · queues","24. Архитектура для High-Load и Low-Latency инференса  ДЗ",null],
  [25,"Гибридная и мультиоблачная архитектура","materials","Hybrid · multi-cloud · portability","25. Гибридная и мультиоблачная архитектура для AI",null],
  [26,"Multi-tenancy в AI SaaS","materials","Isolation · quotas · tenant data","26. Архитектура для Multi-tenancy в AI SaaS",null],
  [27,"Federated Learning и Privacy-Preserving","materials","Privacy · federation · locality","27. Federated Learning и Privacy-Preserving архитектура",null],
  [28,"FinOps: архитектура, управляемая стоимостью","materials","Unit economics · TCO · budgets","28. FinOps архитектура, управляемая стоимостью",null],
  [29,"Технологический радар и эволюция архитектуры","materials","Radar · lifecycle · adoption","29. Технологический радар и эволюция архитектуры",null],
  [30,"Ethical AI by Design и Governance","materials","Governance · Model Card · accountability","30. Ethical AI by Design и архитектура для Governance  ДЗ",null],
  [31,"API как продукт","materials","API product · lifecycle · governance","31. API как продукт проектирование и управление",null]
].map(([id,title,status,evidence,path,expertPath])=>({id,title,status,evidence,path,expertPath}));

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
  const cards = [[31,"уроков"],[7,"контрольных gates"],[counts.done,"подтверждено готовыми"],[counts.review+counts.draft,"в review / draft"],[counts.lab,"рабочих lab-контуров"]];
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
  document.querySelector('#lessonGrid').innerHTML = filtered.length ? filtered.map(l=>{
    const expert=l.expertPath?`<a class="expert-link" href="${l.expertPath}">Эксперт-разбор →</a>`:'';
    return `<article class="lesson-card"><div class="lesson-top"><span class="lesson-no">LESSON ${String(l.id).padStart(2,'0')}</span><span class="badge ${l.status}">${labels[l.status]}</span></div><h3>${l.title}</h3><p>${l.evidence}</p><div class="lesson-links">${expert}<a href="${repoUrl(l.path)}" target="_blank" rel="noopener">Артефакты ↗</a></div></article>`;
  }).join('') : `<div class="empty">По выбранным условиям уроков не найдено.</div>`;
}

function initLinks(){document.querySelectorAll('[data-repo-path]').forEach(a=>a.href=`${REPO}/blob/${BRANCH}/${a.dataset.repoPath.split('/').map(encodeURIComponent).join('/')}`);}
function initTheme(){const root=document.documentElement;const saved=localStorage.getItem('otus-theme');if(saved)root.dataset.theme=saved;document.querySelector('#themeToggle').addEventListener('click',()=>{const next=root.dataset.theme==='light'?'dark':'light';root.dataset.theme=next;localStorage.setItem('otus-theme',next);});}

renderChain(document.querySelector('#heroChain'));renderChain(document.querySelector('#traceChain'));renderStats();renderGates();renderLessons();initLinks();initTheme();
document.querySelector('#lessonSearch').addEventListener('input',renderLessons);document.querySelector('#statusFilter').addEventListener('change',renderLessons);
