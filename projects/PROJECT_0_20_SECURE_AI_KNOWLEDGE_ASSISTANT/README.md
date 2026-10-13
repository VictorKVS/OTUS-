# Сквозной проект 0–20 · Secure AI Knowledge Assistant

## Идея

Один учебно-производственный проект проходит через все уроки 0–20: от идеи и требований до MLOps, GitOps и Canary-релиза.

**Сценарий:** защищённый AI‑ассистент для корпоративной базы знаний. Он принимает вопрос пользователя, проверяет права доступа, извлекает релевантные фрагменты из RAG, формирует ответ с цитатами, применяет security/PII/guardrail policy, пишет audit/telemetry и выпускается как версионированный production release.

## Главный принцип

```text
IDEA
→ REQUIREMENTS
→ ARCHITECTURE
→ RAG / AGENT
→ DATA / INTEGRATIONS
→ EVALUATION
→ SECURITY
→ OBSERVABILITY
→ SIZING
→ IAC / CI/CD / DEVSECOPS
→ MLOPS
→ GITOPS / CANARY / ROLLBACK
```

Каждый этап создаёт артефакты, которые становятся входом следующего. Никаких «нарисовали новую систему на каждом уроке».

## Для кого написано

Документы оформляются на уровне senior engineer/architect, но каждый термин объясняется простым языком. В отчётах используются таблицы, схемы и явное разделение:

- **требование курса**;
- **общеинженерная практика**;
- **проектное решение**;
- **измеренное лабораторное значение**;
- **production threshold**, который нельзя объявлять без production evidence.

## Статус чисел

Цифры не назначаются «для красоты». Для каждого порога указывается происхождение: SLO/error budget, статистический тест, опубликованная практика, benchmark или контролируемый лабораторный эксперимент. До измерения production traffic значение помечается как `LAB` или `DESIGN`, а не как доказанный production факт.

## Структура

| Этап | Результат |
|---:|---|
| 00 | **Идея и паспорт проекта** → PROJECT_CHARTER.md · PROJECT_ID · границы |
| 01 | **Бизнес-контекст** → BUSINESS_CONTEXT.md · SUCCESS_CRITERIA.md |
| 02 | **Требования, оценка и риски** → REQ.md · NFR.md · RISK_REGISTER.md |
| 03 | **Поставка ценности** → DELIVERY_ROADMAP.md · STAGE_GATES.md |
| 04 | **HLD / C4** → C4_CONTEXT.md · C4_CONTAINER.md |
| 05 | **LLD и контракты** → LLD.md · OPENAPI.yaml · SEQUENCE.md |
| 06 | **RAG** → RAG_SPEC.md · RETRIEVAL_POLICY.md |
| 07 | **AI‑агент** → AGENT_SPEC.md · WORKFLOW.md |
| 08 | **ADR** → ADR-*.md |
| 09 | **Архитектурная проверка** → ARCH_REVIEW.md · GAP_REGISTER.md |
| 10 | **Надзор и техдолг** → GOVERNANCE.md · TECH_DEBT.md |
| 11 | **Интеграции** → INTEGRATIONS.md · INTERFACE_CATALOG.md |
| 12 | **Архитектура данных** → DATA_ARCHITECTURE.md · DATA_CLASSIFICATION.md |
| 13 | **Evaluation** → EVAL_PLAN.md · GOLDEN_SET_SPEC.md |
| 14 | **Security by Design** → THREAT_MODEL.md · SECURITY_CONTROLS.md |
| 15 | **Observability** → OBSERVABILITY.md · SLO.md |
| 16 | **Sizing** → SIZING.md · CAPACITY_MODEL.md |
| 17 | **LLM inference sizing** → INFERENCE_PROFILE.md · BENCHMARK_PLAN.md |
| 18 | **IaC + CI/CD + DevSecOps** → PIPELINE.md · IAC.md · SECURITY_GATES.md |
| 19 | **MLOps** → MLOPS_PIPELINE.md · MODEL_REGISTRY.md |
| 20 | **Production release** → DZ20_REPORT.md · CANARY_POLICY.md · ROLLBACK_PLAN.md |

Главный отчёт для сдачи Lesson 20: [REPORT/DZ20_REPORT.md](./REPORT/DZ20_REPORT.md).


## Deepening status

### Wave 1 · Lessons 00–05 — DONE / DESIGN

Created real project artifacts:
- charter/intake;
- business context and measurement plan;
- functional requirements, NFR and risk register;
- value-delivery roadmap and stage gates;
- C4 C1/C2 textual source-of-truth;
- HLD invariants;
- LLD for Query API, OpenAPI 3.1 contract and sequence;
- wave-1 requirements traceability.

Next wave: **06–10 · RAG → Agent → ADR → Architecture Review → Governance**.


## Role in Knowledge Polygon

SAIKA-001 is the **reference project** for the FATHER Knowledge Polygon. Patterns are first made traceable here, then validated against other projects and only after that promoted into reusable FATHER blocks.

See:
- `docs/FATHER_KNOWLEDGE_POLYGON.md`
- `registry/knowledge-polygon.yaml`
- `docs/PORTFOLIO_PHASE_MATRIX.md`
