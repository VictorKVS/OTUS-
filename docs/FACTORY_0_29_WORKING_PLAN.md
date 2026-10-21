# FATHER Factory · рабочий контур по урокам 0–29

## Решение

До дальнейшего расширения курса приоритет — **довести фабрику до рабочего M1-контура на диапазоне 0–29**.

Уроки 30–31 не удаляются из курса, но временно не входят в текущий factory milestone.

## Что означает «рабочая фабрика»

Не просто страница сайта и не список уроков.

Фабрика считается рабочей, когда любой проект проходит один и тот же путь:

```text
INPUT
→ INTAKE
→ ANALYSIS
→ ARCHITECTURE
→ DATA/RAG/AGENT
→ SECURITY + EVALUATION
→ SIZING
→ DEVELOPMENT PACK
→ IMPLEMENTATION
→ CI/QA
→ RELEASE
→ HA/DR + SCALE
→ FINOPS
→ TECHNOLOGY EVOLUTION
→ FEEDBACK
```

и на каждом переходе существуют:
- контракт входа/выхода;
- владелец/станция;
- артефакт;
- test/evidence;
- gate;
- traceability.

## Три рабочие волны

| Волна | Уроки | Что должно заработать |
|---|---:|---|
| W1 | 0–12 | intake, requirements, architecture, RAG/agents, integration, data |
| W2 | 13–20 | eval, security, observability, sizing, IaC/CI/CD, MLOps, production release |
| W3 | 21–29 | HA/DR, platform choice, EDA, high-load, hybrid cloud, multi-tenancy, privacy, FinOps, evolution |

## Почему 21–29 критичны

До Lesson 20 фабрика умеет **сделать и выпустить** систему.

Lessons 21–29 должны научить её **жить после выпуска**:

```text
RELEASE
→ SURVIVE FAILURE
→ CHOOSE RUNTIME
→ REACT TO EVENTS
→ HANDLE LOAD
→ DISTRIBUTE
→ ISOLATE TENANTS
→ PRESERVE PRIVACY
→ CONTROL COST
→ EVOLVE TECHNOLOGY
```

Поэтому G6/G7 — не «добавочные темы», а операционный слой фабрики.

## Lesson 21 — HA / DR

Factory output:
- dependency/failure map;
- HA topology;
- backup policy;
- restore procedure;
- RTO/RPO targets;
- DR drill evidence.

Нельзя писать RTO/RPO как красивые числа: target приходит из business impact, затем подтверждается восстановительным тестом.

## Lesson 22 — Serverless vs Kubernetes

Factory output:
- workload profile;
- decision matrix;
- ADR платформы;
- exceptions.

Выбор должен зависеть от:
- load shape;
- cold-start tolerance;
- state;
- GPU;
- isolation;
- operational team;
- cost model.

## Lesson 23 — EDA

Factory output:
- event catalog;
- AsyncAPI/event schema;
- producer/consumer ownership;
- delivery semantics;
- idempotency;
- retry/DLQ;
- observability contract.

EDA применяется там, где decoupling и async действительно нужны, а не как обязательный стиль для любого сервиса.

## Lesson 24 — High Load / Low Latency

Source assignment gives a concrete scenario: **10,000 RPS and latency < 200 ms**.

Factory must derive:
- cache placement;
- semantic cache policy;
- autoscaling metric;
- queue lane for heavy work;
- optional Geo-DNS/Edge;
- benchmark/load evidence.

Course numbers remain COURSE provenance until our runtime test confirms them.

## Lesson 25 — Hybrid / Multi-Cloud

Factory output:
- placement policy;
- on-prem/cloud boundary;
- data movement policy;
- provider abstraction boundary;
- failover/cost consequences.

## Lesson 26 — Multi-tenancy

Factory output:
- tenant model;
- isolation decision: Silo / Pool / Bridge;
- tenant-aware identity;
- retrieval/data isolation;
- quotas/rate limits;
- tenant observability;
- noisy-neighbor controls.

## Lesson 27 — Federated / Privacy-Preserving

Factory output:
- distributed training topology;
- data-locality boundary;
- privacy control selection;
- aggregation trust model;
- privacy/security evidence.

## Lesson 28 — FinOps

Factory output:
- cost/request and cost/tenant;
- GPU/utilization cost;
- storage/egress cost;
- idle capacity;
- forecast/budget;
- optimization candidates;
- architecture decision with economic evidence.

The lesson asks for a 20% optimization proposal. This is COURSE target, not a promise that every real system can safely cut 20%.

## Lesson 29 — Technology Radar

Factory output:
- Adopt / Trial / Assess / Hold radar;
- evidence for movement between rings;
- owner and review date;
- ADR/debt/backlog links;
- replacement/migration trigger.

Radar becomes the feedback mechanism by which the factory changes its own reusable blocks.

## Итоговая петля

```text
PROJECT
→ FACTORY 0–29
→ RELEASE
→ OPERATIONS
→ EVIDENCE
→ FINOPS / RADAR
→ ADR / BLOCK UPDATE
→ BLOCK REGISTRY
→ NEXT PROJECT
```

Именно после этого FATHER становится не витриной, а самообучающейся инженерной фабрикой.


## FATHER Research & Test Center

Лаборатория является обязательной частью рабочего chassis, а не отдельной демонстрационной страницей.

```text
BASELINE
→ HYPOTHESIS
→ CONTROLLED A/B/N
→ EVALUATION
→ HUMAN SAMPLE REVIEW
→ REGRESSION
→ SAFETY
→ CANARY
→ CHAMPION
→ PRODUCTION
→ REAL-WORLD FEEDBACK
→ NEXT EXPERIMENT
```

Испытываемые типы узлов:
- Model / VLM / Embedding / Reranker;
- Prompt / System Prompt;
- RAG / chunking / retrieval / reranking;
- Knowledge algorithms: fact/entity/relation/provenance/contradiction;
- Agent / Skill / Memory;
- Tool / MCP;
- Workflow / Router;
- Evaluator / Judge;
- Guardrail / Security policy.

Правило фабрики: **ни один challenger не заменяет production champion без воспроизводимого run, versioned dataset, зафиксированных evaluator/metrics, regression suite и evidence.**

### Project Labs

Один `FATHER Experimentation Engine` обслуживает проектные представления:
- FATHER Platform Lab;
- ALINA Research Center;
- OSINT Project Lab;
- последующие IB / Pentest / DevSecOps / Legal / Programmer labs.

### ALINA Research Center

ALINA получает отдельные стенды Prompt Lab, RAG Lab, Knowledge Algorithm Lab, Agent Lab, Skill Lab, Evaluator Lab, Memory Lab и Optimization Lab. Лучшие конфигурации определяются по профилям QUALITY / BALANCED / FAST / LOCAL / SECURE, а не одной универсальной метрикой.


## DevOps / Environment Center precedes Cyber Range

Order is fixed:

```text
FATHER CORE
→ LAB / EVALUATION
→ DEVOPS ENVIRONMENTS
→ CONTAINERS / KUBERNETES
→ CI/CD / GITOPS
→ OBSERVABILITY / SRE
→ ISOLATION / SANDBOX
→ CYBER RANGE
→ ATTACK / DEFENSE AGENTS
```

Cyber Range remains PLANNED until environment gates prove reproducibility, isolation, observability, rollback, security, resource control and retained evidence.

Standard environment profiles:
- LOCAL DEV;
- CONTAINER DEV;
- K8S DEV;
- TEST;
- STAGING;
- PRODUCTION;
- ISOLATED LAB;
- future CYBER RANGE.

The DevOps platform is shared by FATHER, ALINA, OSINT and all later specialist lines; it is not a separate unrelated project.
