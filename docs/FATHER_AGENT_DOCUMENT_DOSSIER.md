# FATHER Agent Document Dossier

Статус: **CANONICAL DESIGN v1**

Agent Dossier — полный комплект документов конкретного агента и его версии.

## 1. Структура досье

~~~text
AGENT_DOSSIER
├── 00_GOVERNANCE      passport · ownership · version · changes · evidence index
├── 01_BUSINESS        intent · requirements · use cases · NFR · risks · traceability
├── 02_ARCHITECTURE    ADR · C4 · component · workflow · state · interfaces · failures
├── 03_INTELLIGENCE    K0 common core · K1 specialist KB · K2 project context · prompts · models · RAG · skills · memory · training
├── 04_SECURITY        threat model · IAM · tool permissions · data · guardrails · abuse
├── 05_DEVELOPMENT     complete validated Development Pack
├── 06_IMPLEMENTATION  code refs · build · schemas · migrations · config · tests · report
├── 07_LAB             datasets · experiments · runs · metrics · regression · safety · multi-LLM
├── 08_DEVOPS          environment · container · K8s/IaC · secrets · observability · rollback
├── 09_ACCEPTANCE      analyst · architect · security · quality · operations
├── 10_CERTIFICATION   certificate · compatibility · limitations · release · Zoo record
└── 11_OPERATIONS      runbook · incidents · RCA · feedback · experience · change requests
~~~

## 2. Agent Passport minimum fields

agent_id, name, family, domain, owner, version, lifecycle status, execution mode, backend, role, goals, prohibited goals, inputs, outputs, common_core_id/version, specialist_pack_ids/versions, optional project_context_id, retrieval/conflict/provenance policies, skill packs, memory scope, models, tools, permissions, workflows, channels, evaluation profile, security profile, supported environments, dependencies, compatibility, cost profile, known limitations, certificate/evidence links.

## 3. Traceability

~~~text
source → requirement → decision → component → implementation → test → experiment → acceptance → certificate → production trace → experience
~~~

## 4. Quality of controlled documents

Каждый документ имеет document id, version, status, owner, approver, date, source references, related requirements, related evidence и change reason.

Document status: DRAFT → REVIEW → APPROVED → BASELINED → SUPERSEDED / DEPRECATED.

## 5. Completeness

Сертификат запрещён, если обязательный раздел отсутствует или BLOCKED. Исключение только через явный N/A с rationale и approver; пустой placeholder не считается N/A.

## 6. Knowledge inheritance

Каждый профессиональный Agent Dossier обязан ссылаться на совместимую версию `FATHER Common Knowledge Core` и минимум один `Specialist Knowledge Pack`. Общая база не копируется внутрь специалиста, а наследуется через Knowledge Router. Полный стандарт: `FATHER_KNOWLEDGE_ARCHITECTURE.md`.
