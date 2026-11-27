# SADEQ — исследование вакансий и backlog MVP на 27 ноября 2026
**Статус:** MARKET RESEARCH / PRIORITIZATION PROPOSED, **НЕ запущена разработка**.

## Границы выборки
Поисковая разведка 27.11.2026: hh.ru (общероссийский/СПб), Хабр Карьера, прямые страницы Greenhouse/Lever, специальный Agentic AI Jobs Index (23.11.2026). Не является исчерпывающей выгрузкой «всех» мировых вакансий; вакансии динамические; доступность по гражданству/стране и реальная remote-eligibility требуют проверки. Индекс Prefactor — собственная выборка, не весь рынок. Некоторые Lever страницы не открылись при повторной проверке, поэтому их требования отмечены **search snippet only**. Не вычисляли процент встречаемости навыков на полной генеральной совокупности.

## Основная мысль
Для карьерной цели Applied AI / AI Security / AI Platform наиболее сильным сигналом станет **не 20 архитектурных диаграмм, а один интегрированный работающий поток с независимыми тестами, source citations, permission checks, observability и измерениями**, подкреплённый HLD/ГОСТ/SEDA.

## Матрица рыночных требований
| Signal | Evidence | MVP response | Priority |
|---|---|---|---|
| Python/FastAPI/typed contracts | QSOFT, AGIMA, DeFacto | runnable backend, strict schema and tests | P0 |
| RAG retrieval/citations/permissions | QSOFT, DeFacto, SberZdorovye | evidence worker, hybrid retrieval, ACL and eval | P0 |
| LangGraph/agent tool/memory | AGIMA, QSOFT, EvolutionIQ | checkpointed workflow and bounded tool calls | P0 |
| AI Security and MCP/tool governance | SberZdorovye, Koronatech, Cirrus Logic | deterministic UAG, negative attack fixture suite | P0 |
| Eval, monitoring, cost/latency | QSOFT, Kobie, Natera, EvolutionIQ | POLYGON runnable test harness + trace dashboards | P0 |
| Enterprise CRM/ERP/webhook automation | DeFacto, Natera, hh automation listings | mock CRM/ticket adapter and documented extension | P1 |
| Full-stack and agentic coding | EvolutionIQ, hh listings, Bell Integrator | approval dashboard + documented verified coding workflow | P1 |
| DevSecOps/K8s/CI | AGIMA, Cirrus, SberZdorovye | Compose first, secure CI; K8s later with evidence | P1 |
| Fine-tuning/advanced ML | Jetlyn; some higher ML roles | controlled research AFTER core works | P2 |

## Role ranking for this profile (qualitative, not market-wide counts)
1. **AI Security Engineer / DevSecOps for AI** — strongest differentiator from combination of existing security expertise and designed UAG+POLYGON. Gap: runnable security gate, real adversarial results.
2. **Applied AI / LLM-RAG Engineer** — broadest overlapping applied stack. Gap: shipped end-to-end demo and measured evals.
3. **Enterprise AI Integration / Forward-Deployed AI Engineer** — domain fit and real business integration. Gap: API/MCP/CRM integrations, n8n or Make exercise, business KPI.
4. **AI Platform Engineer** — defensible architecture and security; hands-on OTel/CI/infra missing.
5. **AI Architect** — strong documented design; needs workload benchmarks and independent engineering review.
6. **Fine-Tuning ML Researcher** — lower immediate value to stated MVP and highest retraining gap.

## Explicit sample of vacancies and citations
- **VAC-01 QSOFT — Python-разработчик AI-сервисов (LLM/RAG)** (RU, remote): FastAPI;asyncio;RAG;Qdrant;LangGraph;multi-tenant ACL;Ollama;OTel;Langfuse;pytest. [Source](https://career.habr.com/vacancies/1000169407?f=company_vacancies).
- **VAC-02 СберЗдоровье — Специалист по кибербезопасности AI/LLM** (RU, Moscow): Threat modelling;prompt injection;RAG poisoning;agent tool ACL;SIEM;Kubernetes security;human approval. [Source](https://career.habr.com/vacancies/1000168651).
- **VAC-03 AGIMA — Senior AI Engineer (Python/LLM/AI Agents)** (RU, remote/hybrid): Multi-step workflows;memory;orchestration;eval;guardrails;observability;Python async;Docker/K8s. [Source](https://career.habr.com/vacancies/1000170599).
- **VAC-04 ДеФакто — AI Engineer/Python Developer** (RU, listing has remote flag but states office; verify with employer): Documents;integration;pilot;FastAPI;MCP;tool call;RAG;eval;prompt injection. [Source](https://career.habr.com/vacancies/1000170305?f=company_vacancies).
- **VAC-05 Джетлин — ML Engineer GenAI/CV** (RU, remote): ML validation;A/B;evals;fine-tuning;agent state;human-in-the-loop;MLOps. [Source](https://career.habr.com/vacancies/1000169302).
- **VAC-06 Koronatech — DevSecOps AI tools** (RU, remote indicated by HH search): AI agents;MCP server security;AI gateways;threat modelling. [Source](https://hh.ru/search/vacancy?text=DevSecOps%20%28%D0%B1%D0%B5%D0%B7%D0%BE%D0%BF%D0%B0%D1%81%D0%BD%D0%BE%D1%81%D1%82%D1%8C%20AI-%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%29).
- **VAC-07 EvolutionIQ — AI Engineer Agentic** (USA, location/eligibility must verify): Deterministic workflows;durable agent checkpoint;event sourcing;evals;guardrails;trace;graph;Python+TS. [Source](https://job-boards.greenhouse.io/evolutioniq/jobs/6242824004).
- **VAC-08 Natera — Forward Deployed AI Solutions Engineer** (USA, US Remote only): Workflow mapping;enterprise MCP/API/webhooks;human approval;business KPIs;eval;observability. [Source](https://job-boards.greenhouse.io/natera/jobs/6115022004).
- **VAC-09 Cirrus Logic — AI Platform Engineer** (Intl, hybrid on-prem/cloud, location verify): AI Gateway;MCP/skill registry;OIDC;K8s/GitOps;monitoring;quotas;security. [Source](https://jobs.eu.lever.co/cirrus/29d39dda-5b26-4b06-afc8-34f139a8f35c).
- **VAC-10 Kobie Marketing — Lead AI QA Engineer** (Intl, location/eligibility verify): RAG correctness;JSON schema;tool regression;Ragas/DeepEval/Langfuse;trace assertions. [Source](https://jobs.lever.co/kobie/3280d456-5db2-4070-a7eb-d879c17c1393).
- **VAC-11 Creatio — AI Engineer** (Intl, listing URL not currently fetchable): Enterprise agents;context/memory/permissions;eval;HITL;AI coding. [Source](https://jobs.eu.lever.co/creatio/2c0c0c2d-cffb-40db-8b38-0068aefa1696).
- **VAC-12 DoorDash — ML Platform GenAI Engineer** (USA, location/eligibility verify): Agent or MCP server deployment;eval;observability;tracing;RAG platform. [Source](https://job-boards.greenhouse.io/doordashusa/jobs/8264542).
- **VAC-13 Битрикс/automation sample — AI automation/integrations** (RU, remote listings varying): n8n;Make;CRM/ERP;webhooks;REST;Python;workflow. [Source](https://hh.ru/search/vacancy?text=AI%20Automation%20Engineer%20n8n%20Make).
- **VAC-14 SPB aggregate — Специалист по внедрению ИИ/автоматизации** (RU, Saint Petersburg): AI agents pet projects;backend/UI;integration;business workflows. [Source](https://spb.hh.ru/search/vacancy?text=%D0%B2%D0%BD%D0%B5%D0%B4%D1%80%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%98%D0%98%20%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%B0%D1%82%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F).

## Proposed P0/P1/P2 capability backlog
### P0-01 RAG Knowledge Worker
Document import PDF/DOCX;chunk and provenance;hybrid retrieve;source citations;ACL;golden query set;relevance metrics

**Acceptance:** OpenAI-independent local inference; at least two source types; deterministic access deny; compare to vector baseline. **Job mapping:** QSOFT;DeFacto;AGIMA;Natera. **SADEQ reference:** ALG-01,07.

### P0-02 Agent Workflow & Tool-use
LangGraph checkpoint;state machine;strict tool schema;bounded loops;retry/idempotency;human approval

**Acceptance:** Simulate enterprise ticket → proposal → approval → mock-ERP update → actual state verification. **Job mapping:** AGIMA;EvolutionIQ;Natera. **SADEQ reference:** ALG-02,04,05,10,11,12.

### P0-03 AI Security Gateway / UAG
OIDC or demo identities;RBAC/ABAC;tenant isolation;MCP or OpenAPI allowlisted tools;prompt injection fixture suite

**Acceptance:** User B blocked across RAG/cache/graph/tools; prompt injection cannot call forbidden tools. **Job mapping:** SberZdorovye;Koronatech;QSOFT. **SADEQ reference:** ALG-01,03,07,11.

### P0-04 POLYGON eval harness
golden dataset;RAG groundedness and retrieval;tool trajectory checks;regression on model/prompt change;CI gate

**Acceptance:** One reproducible eval command; report by version/hash; pass/fail evidence; demonstrate deliberate failing revision. **Job mapping:** QSOFT;Kobie;EvolutionIQ;Natera. **SADEQ reference:** ALG-07,08,10,12.

### P0-05 Observable local deployment
Python FastAPI;PostgreSQL;Qdrant;Ollama;Docker Compose;OTel/trace/cost/latency;tests

**Acceptance:** Fresh-machine deployment runbook; measured TTFT/p95; all calls local with deny egress test. **Job mapping:** QSOFT;AGIMA;Cirrus Logic. **SADEQ reference:** B08.

### P1-06 Enterprise integration adapter
1C/Bitrix24/CRM mock or controlled test account;webhooks;API versioning;OpenAPI/MCP adaptor

**Acceptance:** From event to approved business ticket and verified update; 2 connector types. **Job mapping:** DeFacto;Natera;RU automation jobs. **SADEQ reference:** ALG-01,11,12.

### P1-07 Corporate UI
React+TypeScript or simple UI;citations;approval queue;trace view;health and errors

**Acceptance:** Reviewer can see evidence and reject/approve exact action; don't claim full-stack without implementation. **Job mapping:** EvolutionIQ;Natera;SPB AI implementation roles. **SADEQ reference:** B01,B05,B08.

### P1-08 DevSecOps pipeline
GitHub Actions/GitLab CI;SAST/SCA/secret scan;SBOM;image signing;K8s/Helm optional

**Acceptance:** CI fails on intentionally vulnerable fixture; deployment validated; rollback demo. **Job mapping:** Cirrus Logic;QSOFT;SberZdorovye. **SADEQ reference:** SEC03/B08.

### P2-09 GraphRAG + alternate algorithms
Compare vector-only/hybrid vs graph traversal on relationship questions; index cost and quality

**Acceptance:** Graph only if adds measured value and can cite graph paths. **Job mapping:** QSOFT;EvolutionIQ. **SADEQ reference:** ALG-07.

### P2-10 Model tuning and advanced ML
LoRA;classical forecasting;A/B;model routing;MLflow

**Acceptance:** Only after baseline MVP and genuine dataset/compute need. **Job mapping:** Jetlyn. **SADEQ reference:** ALG-09.

### P2-11 Multi-agent agent factory
Specialized 3 profiles; Agent 001 code patch in sandbox; independent qualification

**Acceptance:** No core duplication; no candidate can approve itself; not needed before working agent flow. **Job mapping:** AGIMA;D&B;Cirrus Logic. **SADEQ reference:** B06/B07.


## First showcase workflow (cross-role evidence)
**Corporate incident / maintenance request assistant** on synthetic documentation + tickets; use healthcare operational IT or standard enterprise IT procedures without medical diagnosis or personal data. Input: ticket/email plus incident rules; local model; retrieval from authorized source; explain cited answer; suggest action via typed tool; human approval; update mock ticketing service; verify state; negative test prompt injection/tenant leak; evaluate Q/A, tool correctness, latency/cost; show traces and evidence in dashboard. Non-security audiences see helpful business automation, security audiences see governance, AI engineers see real RAG/agent code.

## Decision gate before writing code
Choose one demo domain; baseline dataset with license and synthetic PII-free records; define 10–20 business acceptance cases and 20+ negative tests (planned targets, not achieved); freeze contract; select Compose and on-prem Ollama first. GraphRAG/Neo4j should be retained as **optional measured add-on**, not block MVP if hybrid retrieval meets scenario; however older SADEQ/OTUS requirements require real GraphRAG for final project, so sequence it as a distinct qualifying stage before OTUS final acceptance. No 10k inference RPS claim.

## Source limitations
HH search results are dynamic aggregator snippets; where an individual vacancy URL was not accessible, the evidence is weaker and only indicates themes. Closed or geo-restricted roles must not be represented as available to the user. International compensation cannot be compared to RU net without tax/eligibility adjustment. This report is for **backlog design**, not job application action.
