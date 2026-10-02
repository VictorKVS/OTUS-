# FATHER Production Base — Minimum v1

Статус: **SCAFFOLD / M0**

Сайт является производственной базой проекта. OTUS остаётся источником методов/уроков, но основной runtime сайта — проектный конвейер.

## Minimum principle

На каждой стадии уже должны существовать:
- назначенный агент;
- agent manifest;
- system prompt;
- RAG profile;
- knowledge-base bindings;
- вход/выход;
- gate;
- trace/evidence contract.

Это **наличие каркаса**, не утверждение, что агенты уже production-ready.

## Core chain

`SUPERVISOR → INTAKE → ANALYST → ARCHITECT → CROSS-CUTTING SPECIALISTS → DEV PACK → PRE-DEV VALIDATOR → PROGRAMMER → QA → ACCEPTANCE → RELEASE → OPS`

Transversal:
- Knowledge Curator;
- Governance / Traceability;
- Security;
- Quality/Eval;
- Sizing/FinOps.

## Knowledge plane

Минимально зарегистрированы:
- `KB-SOURCES` — Source & Intake Corpus;
- `KB-PROJECT` — Canonical Project KB;
- `KB-REQUIREMENTS` — Requirements KB;
- `KB-ARCHITECTURE` — Architecture KB;
- `KB-DATA` — Data & Integration KB;
- `KB-SECURITY` — Security KB;
- `KB-REGULATORY` — Regulatory / Policy KB;
- `KB-QUALITY` — Quality / Eval KB;
- `KB-OPERATIONS` — Operations / SRE KB;
- `KB-FINOPS` — Sizing / FinOps KB;
- `KB-CODE` — Code / Engineering KB;
- `KB-TRACE` — Traceability Graph;
- `KB-EVIDENCE` — Evidence Store;

## RAG baseline

Каждый агент:
- hybrid retrieval;
- top_k=8;
- reranker;
- citations/provenance required;
- project_id filter;
- approved/baselined/verified documents by default;
- raw sources only for Intake/Knowledge Curator;
- empty retrieval → GAP, not invention;
- conflict → finding, not silent resolution.

## Prompt baseline

Каждый role prompt:
- ограничивает зону ответственности;
- различает fact / assumption / hypothesis / decision / GAP;
- требует evidence/source refs;
- запрещает silent baseline change;
- возвращает structured status/findings/next owner.

## Current maturity

Все созданные agents/KB/RAG/prompt contracts имеют статус `scaffold / M0`.

Следующие уровни:
- M1 — filled project-specific prompts and KB routing;
- M2 — tested agent workflows/evals;
- M3 — automated runtime with observability/security/cost gates.
