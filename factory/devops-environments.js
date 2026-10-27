const environments=[
 {icon:'💻',name:'LOCAL DEV',status:'REAL/DESIGN',cls:'real',desc:'Windows/WSL/Linux workstation, IDE, local models, unit tests.'},
 {icon:'🐳',name:'CONTAINER DEV',status:'DESIGN',cls:'design',desc:'Docker/Compose profiles for agents, APIs, DB, vector store and tools.'},
 {icon:'☸',name:'K8S DEV',status:'IN PROGRESS',cls:'design',desc:'Minikube/local cluster for manifests, networking, storage and resource tests.'},
 {icon:'🧪',name:'TEST',status:'PLANNED',cls:'planned',desc:'Automated integration, eval, contract and regression runs.'},
 {icon:'🎭',name:'STAGING',status:'PLANNED',cls:'planned',desc:'Production-like environment for release candidate and canary checks.'},
 {icon:'🚀',name:'PRODUCTION',status:'PLANNED',cls:'planned',desc:'Controlled runtime with SLO, approvals, rollback and audit.'},
 {icon:'🔒',name:'ISOLATED LAB',status:'PLANNED',cls:'planned',desc:'Restricted network, disposable workloads and unsafe-tool containment.'},
 {icon:'⚔',name:'CYBER RANGE',status:'FUTURE',cls:'planned',desc:'Attack/Defense agents only after isolation and observability are proven.'}
];
const platform=[
 ['🐳','Containers','Images, registries, SBOM, image scanning and immutable runtime units.'],
 ['☸','Kubernetes','Deployments, Services, Ingress, NetworkPolicy, RBAC, quotas and namespaces.'],
 ['🔁','CI/CD','Build, test, eval, security scan, artifact promotion and release evidence.'],
 ['🌿','GitOps','Desired state in Git, environment promotion, drift detection and rollback.'],
 ['🔐','Secrets','Secret stores, rotation, least privilege and no credentials in repositories.'],
 ['📦','Artifacts','Container images, model artifacts, prompts, datasets and signed versions.'],
 ['🗄','Data Services','PostgreSQL, vector DB, object storage, queues/event bus and backups.'],
 ['📡','Observability','OpenTelemetry-style traces, logs, metrics, dashboards and alerting.'],
 ['📏','SRE/SLO','Availability, latency, error budgets, capacity and incident readiness.'],
 ['💰','FinOps','Cost/request, GPU utilization, environment spend and optimization evidence.'],
 ['🛡','DevSecOps','SAST/SCA/container/IaC/secrets/policy checks as delivery gates.'],
 ['🧱','Sandboxing','Ephemeral environments, network isolation, resource limits and snapshots.']
];
const gates=[
 ['G-ENV-01','Reproducibility','Environment is recreated from code/config, not manual clicks.'],
 ['G-ENV-02','Isolation','Project/tenant/test workloads have explicit network and permission boundaries.'],
 ['G-ENV-03','Observability','Every run exposes logs, metrics, traces and correlation IDs.'],
 ['G-ENV-04','Rollback','Release and state recovery procedure is tested, not merely documented.'],
 ['G-ENV-05','Security','Secrets, images, dependencies and IaC pass automated security checks.'],
 ['G-ENV-06','Resources','CPU/RAM/GPU/storage quotas and limits are declared and observable.'],
 ['G-ENV-07','Evidence','Build/test/deploy results are retained and linked to version/commit.'],
 ['G-ENV-08','Lab Safety','Potentially dangerous experiments use disposable isolated environments.']
];
const chain=['CODE / CONFIG','BUILD','UNIT / CONTRACT','AI EVAL','SECURITY','IMAGE / ARTIFACT','DEV','TEST','STAGE','CANARY','PROD','OBSERVE','FEEDBACK'];
document.querySelector('#envGrid').innerHTML=environments.map(x=>'<article class="env-card"><div class="icon">'+x.icon+'</div><div class="meta">'+x.name+'</div><h3><span class="env-status '+x.cls+'">'+x.status+'</span></h3><p>'+x.desc+'</p></article>').join('');
document.querySelector('#platformGrid').innerHTML=platform.map(x=>'<article class="platform-card"><div class="icon">'+x[0]+'</div><h3>'+x[1]+'</h3><p>'+x[2]+'</p></article>').join('');
document.querySelector('#gateGrid2').innerHTML=gates.map(x=>'<article class="gate-card"><div class="meta">'+x[0]+'</div><h3>'+x[1]+'</h3><p>'+x[2]+'</p></article>').join('');
document.querySelector('#deliveryLane').innerHTML=chain.map((x,i)=>'<div class="step"><b>'+x+'</b></div>'+(i<chain.length-1?'<span class="arrow">→</span>':'')).join('');