# FATHER Development Pack Standard

Статус: **CANONICAL v1**

Development Pack — единственный допустимый task-scoped вход программиста.

Путь:

`BASELINED ANALYSIS → APPROVED ARCHITECTURE → DEVELOPMENT PACK → PRE-DEV VALIDATION → PROGRAMMER`

Программист не должен начинать реализацию по чату, голосовому сообщению, одному PRD, одной схеме или набору несвязанных файлов.

## 1. Что именно получает программист

Корень пакета:

```text
04_dev_pack/
├── DEV_PACK_MANIFEST.json
├── DEV_TASK.md
├── REQUIREMENTS_SLICE.yaml
├── ACCEPTANCE_CRITERIA.md
├── LLD_COMPONENT.md
├── SEQUENCE.md
├── openapi.yaml
├── schemas/
│   └── *.schema.json
├── DATA_MODEL_SLICE.md
├── SECURITY_CONSTRAINTS.md
├── OBSERVABILITY_REQUIREMENTS.md
├── QUALITY_GATES.yaml
├── TEST_PLAN.md
├── CONFIG_CONTRACT.yaml
├── MIGRATION_PLAN.md
├── ROLLBACK_PLAN.md
├── RELATED_ADR.md
├── TRACEABILITY_SLICE.json
└── PRE_DEV_VALIDATION_REPORT.md
```

## 2. DEV_PACK_MANIFEST.json

Содержит:
- pack_id;
- project_id;
- task_id;
- version;
- status;
- analyst_signoff;
- architect_signoff;
- required_documents;
- requirement_ids;
- related_adr_ids;
- API/schema versions;
- security classification;
- pre_dev_gate status.

Статус `ready_for_development` запрещён без analyst + architect sign-off и зелёного validation report.

## 3. DEV_TASK.md

Программист должен увидеть за 2–3 минуты:
- цель;
- что сделать;
- что не входит в scope;
- входы/выходы;
- зависимости;
- ограничения;
- acceptance summary;
- ссылки на requirement IDs;
- Definition of Done.

## 4. REQUIREMENTS_SLICE.yaml

Только требования, относящиеся к данной задаче.

Каждый элемент:
- id;
- type = FR/NFR;
- statement;
- rationale;
- source_ref;
- priority;
- owner;
- acceptance_ids;
- status = baselined.

## 5. ACCEPTANCE_CRITERIA.md

Каждый criterion:
- AC-ID;
- связанный REQ-ID;
- Given / When / Then либо эквивалентная однозначная форма;
- expected result;
- negative case;
- measurable threshold, если применимо;
- evidence required.

## 6. LLD_COMPONENT.md

Обязательно:
- responsibility;
- boundaries;
- dependencies;
- public interfaces;
- internal modules;
- state;
- failure modes;
- concurrency model;
- security hooks;
- telemetry hooks;
- config inputs.

## 7. SEQUENCE.md

Минимум:
- happy path;
- error path;
- timeout/retry path;
- authorization/policy path;
- idempotency/duplicate path, если применимо.

## 8. openapi.yaml / asyncapi.yaml

До программиста контракт уже должен:
- парситься;
- иметь version;
- иметь request/response schemas;
- иметь error responses;
- иметь auth scheme, если нужен;
- ссылаться на canonical schemas.

## 9. schemas/

JSON Schema / payload contracts:
- required fields;
- types;
- enums;
- formats;
- nullable policy;
- version;
- backward compatibility note.

## 10. DATA_MODEL_SLICE.md

- entities;
- keys;
- relations;
- indexes;
- retention;
- ownership;
- PII/secret classification;
- migrations;
- consistency rules.

## 11. SECURITY_CONSTRAINTS.md

Программист получает не «сделать безопасно», а конкретно:
- authn/authz;
- roles/scopes;
- input validation;
- PII/DLP policy;
- secrets handling;
- encryption requirements;
- prompt/tool policy for AI;
- audit events;
- prohibited operations;
- abuse/negative scenarios.

## 12. OBSERVABILITY_REQUIREMENTS.md

До разработки определяются:
- metric names;
- labels;
- log events;
- trace spans;
- correlation/request IDs;
- SLI/SLO relation;
- alert owner;
- dashboard expectation;
- privacy/redaction rules.

## 13. QUALITY_GATES.yaml

Hard gates:
- unit;
- integration;
- contract;
- security;
- schema;
- AI/RAG eval if applicable;
- performance if applicable;
- lint/type;
- SAST/SCA/secret scan.

Для AI дополнительно:
- faithfulness/relevancy or task-specific quality;
- retrieval metrics;
- prompt regression;
- unsafe action / leakage hard gates.

## 14. TEST_PLAN.md

До первой строки production code должны быть описаны:
- unit tests;
- integration tests;
- contract tests;
- negative tests;
- authorization tests;
- security tests;
- data migration tests;
- load/performance tests;
- AI eval / RAG eval;
- observability verification;
- rollback verification.

## 15. CONFIG_CONTRACT.yaml

- config key;
- type;
- required/default;
- allowed range;
- secret/non-secret;
- environment scope;
- reload/restart behavior.

## 16. MIGRATION_PLAN.md

Если миграции нет — явно `N/A`.

Если есть:
- forward migration;
- validation;
- compatibility window;
- backfill;
- rollback/recovery;
- data loss risk.

## 17. ROLLBACK_PLAN.md

- rollback trigger;
- artifact/version;
- data compatibility;
- migration reversal or restore;
- feature flag;
- owner;
- maximum recovery time.

## 18. RELATED_ADR.md

Только релевантные ADR:
- ADR-ID;
- decision;
- constraints for implementation;
- forbidden alternatives;
- review trigger.

## 19. TRACEABILITY_SLICE.json

Минимальная цепь для каждого REQ:

`REQ → ADR/CMP/API/DATA → CTRL → TEST → ACCEPTANCE → TELEMETRY/SLO`

## 20. PRE_DEV_VALIDATION_REPORT.md

Генерируется до handoff программисту.

Категории:

### P0 Completeness
Все обязательные документы присутствуют и не пусты.

### P1 Sign-off
Analyst и Architect status = approved.

### P2 Requirements
Каждый REQ-ID существует, baselined и имеет acceptance.

### P3 Acceptance
Каждый AC связан с REQ; criteria тестируемы.

### P4 Contract
OpenAPI/AsyncAPI/schema согласованы; versions/errors/auth определены.

### P5 Data
Сущности/ключи/relations/migration/retention определены либо явно N/A.

### P6 Security
Auth, secrets, PII/data classification, audit, abuse/negative cases определены.

### P7 Observability
Metrics/logs/traces/correlation/SLO-owner определены.

### P8 Tests
Unit/integration/contract/negative/security + applicable performance/AI eval определены.

### P9 Operations
Config, migration, rollback, capacity constraints определены.

### P10 Traceability
Нет orphan requirements, orphan tests или orphan controls.

### P11 Hygiene
Нет unresolved `TODO`, `TBD`, `???`, пустых owners или неизвестных critical decisions.

## Gate result

`PASS` → programmer receives pack.

`FAIL` → пакет возвращается владельцу finding-а:
- requirements → Analyst;
- architecture/API/data → Architect;
- security → Security;
- SLO/observability → SRE/Architect;
- tests/eval → QA/AI Quality;
- sizing/cost → Architect/FinOps.

## Definition of Ready for Programmer

Программист получает задачу только если:

```text
AnalystSignoff == APPROVED
AND ArchitectSignoff == APPROVED
AND PreDevValidation == PASS
AND CriticalOpenQuestions == 0
AND OrphanRequirements == 0
AND OrphanAcceptance == 0
AND ContractValidation == PASS
AND SecurityGate == PASS
AND TestPlanGate == PASS
AND RollbackDefined == TRUE
```

## Handoff

В интерфейсе сайта кнопка **"Передать программисту"** должна быть disabled, пока Gate != PASS.

После PASS фиксируются:
- pack version;
- git commit SHA;
- validator version;
- sign-off timestamps;
- immutable validation report.

Любое изменение baselined REQ/API/schema/security constraint после handoff → новая версия Development Pack и повторный PRE-DEV VALIDATION.
