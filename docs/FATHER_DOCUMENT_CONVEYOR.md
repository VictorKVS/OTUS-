# FATHER Document Conveyor

Статус: **CANONICAL v1**

Назначение: единый производственный конвейер документов FATHER от сырого входа до Development Pack, реализации, проверки и релиза.

Главная трассировка проекта:

`BUS → REQ/NFR → RISK → ADR → CMP/INT/DATA → CTRL/SAFE → TEST/EVAL → SLO/OBS → COST/FIN → DEPLOY/RUN → REL`

## 0. Вход проекта — Intake Pack

### Что может прийти на вход

- идея / поручение / бизнес-задача;
- письмо, договорённость, ТЗ заказчика;
- PDF/DOCX/XLSX/схемы;
- существующий код / Git repository;
- API documentation;
- нормативные и внутренние документы;
- screenshots / видео / прототипы;
- данные / выгрузки / примеры;
- ограничения по срокам, бюджету, инфраструктуре и безопасности.

### Канонические документы Intake

1. `PROJECT_PASSPORT.md`
2. `SOURCE_REGISTER.md`
3. `STAKEHOLDER_REGISTER.md`
4. `BUSINESS_CONTEXT.md`
5. `GLOSSARY.md`
6. `CONSTRAINTS.md`
7. `ASSUMPTIONS_OPEN_QUESTIONS.md`
8. `DATA_SECURITY_CLASSIFICATION.md`
9. `INITIAL_SCOPE.md`
10. `SUCCESS_CRITERIA.md`

### Gate I0 — Intake Ready

Вход считается готовым к аналитике, если:
- источник каждого факта известен;
- неизвестные не выданы за факты;
- определены границы задачи;
- определены владелец/заказчик и ожидаемый результат;
- чувствительные данные классифицированы хотя бы предварительно.

---

## 1. Аналитик — Analysis Pack

Аналитик превращает сырой Intake Pack в проверяемую модель задачи.

### Основные документы

1. `AS_IS.md` — текущее состояние.
2. `TO_BE.md` — целевое состояние с точки зрения бизнеса/пользователя.
3. `BUSINESS_PROCESS.bpmn` / BPMN.
4. `USE_CASES.md` / user stories / scenarios.
5. `FUNCTIONAL_REQUIREMENTS.yaml` — FR-001...
6. `NFR.yaml` — NFR-001...
7. `DATA_CATALOG.md` — сущности, владельцы, качество, классы данных.
8. `INTEGRATION_REGISTER.md` — внешние/внутренние системы.
9. `RISK_REGISTER.md`.
10. `ASSUMPTIONS_OPEN_QUESTIONS.md` — обновлённый.
11. `TRACEABILITY_MATRIX.csv/json`.
12. `ANALYSIS_DECISIONS.md`.
13. `ANALYSIS_REVIEW.md`.

### Правило аналитика

Каждое требование обязано иметь:
- ID;
- источник;
- rationale;
- acceptance criterion;
- priority;
- owner;
- связи с данными/процессом;
- статус: fact / assumption / hypothesis / decision.

### Gate A1 — Analyst Self Review

Аналитик сам проверяет:
- полноту;
- противоречия;
- дубли;
- терминологию;
- отсутствующие acceptance criteria;
- непроверенные предположения;
- traceability до источника.

Результат: **Analysis Pack v1**.

---

## 2. Архитектор — Independent Review

Архитектор не переписывает требования «по своему пониманию». Он принимает Analysis Pack как вход и проводит независимую проверку реализуемости.

### Документы архитектурной проверки

1. `ARCHITECT_REVIEW.md`
2. `REQUIREMENT_GAPS.md`
3. `QUALITY_ATTRIBUTE_SCENARIOS.md`
4. `ARCHITECTURE_OPTIONS.md`
5. `TRADEOFF_MATRIX.md`
6. `ARCHITECTURE_RISKS.md`
7. `ADR/ADR-NNNN.md`
8. `C4_CONTEXT.md/svg`
9. `C4_CONTAINER.md/svg`
10. `ARCHITECTURE_VISION.md`

### Gate A2 — Analyst ↔ Architect Handshake

Перед дальнейшим проектированием должны быть два независимых подтверждения:

**Analyst sign-off**
- архитектура не исказила бизнес-смысл;
- все обязательные сценарии сохранены;
- требования и acceptance criteria не потеряны.

**Architect sign-off**
- требования технически реализуемы;
- NFR измеримы;
- ключевые trade-offs и риски зафиксированы;
- критические решения оформлены ADR.

Только после этого Analysis Pack становится **BASELINED**.

---

## 3. Детальное проектирование — Architecture Pack

После baseline архитектор/AI architect формирует техническую модель решения.

### Core Architecture

1. `C4_COMPONENT.md/svg`
2. `SEQUENCE_*.md/svg`
3. `DEPLOYMENT.md/svg`
4. `DATA_FLOW_DFD.md/svg`
5. `COMPONENT_CATALOG.yaml`
6. `INTERFACE_CATALOG.yaml`
7. `ERROR_MODEL.md`

### API / Integration

8. `api/openapi.yaml`
9. `api/asyncapi.yaml` — если применимо.
10. `schemas/*.json`
11. `EVENT_CATALOG.yaml`
12. `RETRY_DLQ_IDEMPOTENCY.md`

### Data / AI

13. `DATA_MODEL.md`
14. `RAG_SPEC.yaml`
15. `PROMPT_CONTRACT.yaml`
16. `AGENT_SPEC.yaml`
17. `MEMORY_POLICY.yaml`
18. `MODEL_ROUTING.yaml`
19. `TOOL_MCP_POLICY.yaml`
20. `EVIDENCE_CITATION_POLICY.md`

Результат: **Architecture Pack v1**.

---

## 4. Cross-cutting review

До программиста решение проходит сквозные контуры.

### Security Pack

- `DATA_CLASSIFICATION.md`
- `THREAT_MODEL.md`
- `SECURITY_CONTROLS.yaml`
- `IAM_MATRIX.md`
- `SECRETS_POLICY.md`
- `DLP_PII_POLICY.md`
- `AUDIT_REQUIREMENTS.md`
- `SECURITY_TEST_PLAN.md`

### Quality / AI Eval Pack

- `TEST_STRATEGY.md`
- `GOLDEN_DATASET.md/jsonl`
- `RAG_EVAL_PLAN.md`
- `PROMPT_EVAL_PLAN.md`
- `RED_TEAM_PLAN.md`
- `QUALITY_GATES.yaml`

### Operations Pack

- `SLO_SLI.md`
- `OBSERVABILITY_CONTRACT.md`
- `ALERT_MATRIX.md`
- `RUNBOOKS/`
- `CAPACITY_SIZING.md/xlsx`
- `INFERENCE_PROFILE.yaml`
- `TCO_FINOPS.md/xlsx`
- `HA_DR.md`
- `ROLLBACK_REQUIREMENTS.md`

### Gate A3 — Architecture Review / CTO Challenge

Проверяется:
- соответствие baseline requirements;
- security;
- data;
- RAG/agent quality;
- observability;
- SLO;
- capacity;
- cost;
- reliability;
- operability.

Результат: **APPROVED FOR DEVELOPMENT** либо findings/rework.

---

## 5. Development Pack — что получает программист

Программист **не получает сырой архив всех документов как основное задание**.

Из canonical packs формируется компактный task-scoped пакет.

### Обязательные файлы Development Pack

1. `DEV_PACK_MANIFEST.json`
2. `DEV_TASK.md`
3. `REQUIREMENTS_SLICE.yaml`
4. `ACCEPTANCE_CRITERIA.md`
5. `LLD_COMPONENT.md`
6. `SEQUENCE.md`
7. `openapi.yaml / asyncapi.yaml`
8. `schemas/`
9. `DATA_MODEL_SLICE.md`
10. `SECURITY_CONSTRAINTS.md`
11. `OBSERVABILITY_REQUIREMENTS.md`
12. `QUALITY_GATES.yaml`
13. `TEST_PLAN.md`
14. `CONFIG_CONTRACT.yaml`
15. `MIGRATION_PLAN.md` — если нужно.
16. `ROLLBACK_PLAN.md`
17. `RELATED_ADR.md`
18. `TRACEABILITY_SLICE.json`

### Definition of Ready for Developer

Задача не передаётся программисту, пока:
- нет открытого critical ambiguity;
- интерфейсы согласованы;
- acceptance criteria тестируемы;
- security constraints известны;
- schema/versioning определены;
- error cases определены;
- нужные ADR приняты;
- Dev Pack подписан Analyst + Architect.

---

## 6. Программист — Implementation Pack

Программист возвращает:

- код;
- unit tests;
- integration tests;
- contract tests;
- migrations;
- config/env examples без secrets;
- README / run instructions;
- telemetry hooks;
- changelog;
- PR;
- build artifacts;
- предложение нового ADR, если реализация требует изменения архитектуры.

### Запрещённый путь

`Developer discovers architecture ambiguity → silently chooses implementation`

Правильный путь:

`ambiguity → finding → Analyst/Architect review → ADR/requirement update → refreshed Dev Pack → code`

---

## 7. Автоматическая техническая проверка

CI/CD проверяет:
- build;
- lint/type checks;
- unit/integration/contract tests;
- SAST/SCA/secret scan;
- schema/OpenAPI validation;
- RAG/LLM eval;
- security tests;
- load/performance where needed;
- container/IaC validation;
- traceability/evidence completeness.

Результат: **Implementation Evidence Pack**.

---

## 8. Повторная проверка аналитиком

Аналитик проверяет:
- реализованы ли FR;
- сохранён ли смысл use cases;
- acceptance criteria выполнены;
- нет ли scope drift;
- корректны ли пользовательские тексты/сценарии/данные.

Результат: `ANALYST_ACCEPTANCE.md`.

---

## 9. Повторная проверка архитектором

Архитектор проверяет:
- architecture conformance;
- NFR/SLO;
- API/data contracts;
- security controls;
- observability;
- capacity;
- cost;
- reliability;
- deviations/debt.

Результаты:
- `ARCHITECT_ACCEPTANCE.md`;
- `DEBT_REGISTER.md`;
- `WAIVERS.md` при необходимости.

---

## 10. Release Pack

В релиз идут:

1. `RELEASE_MANIFEST.json`
2. `RELEASE_NOTES.md`
3. `CHANGELOG.md`
4. `DEPLOYMENT_PLAN.md`
5. `ROLLBACK_PLAN.md`
6. `RUNBOOKS/`
7. `SLO_DASHBOARD_LINKS.md`
8. `SECURITY_EVIDENCE.md`
9. `TEST_EVIDENCE.md`
10. `KNOWN_ISSUES.md`
11. `TRACEABILITY_SNAPSHOT.json`
12. versioned Architecture Pack / ADR references.

Gate: **RELEASE APPROVED**.

---

## 11. Production feedback loop

`Production telemetry / incidents / user feedback → findings → regression dataset → requirement/risk → ADR if needed → new Dev Pack → next release`

Ошибка не должна исчезать в истории:
- production failure → regression test;
- security event → red-team case;
- retrieval failure → RAG eval case;
- user rejection → acceptance scenario;
- capacity incident → sizing model update.

---

# Каноническая структура проекта

```text
project/
├── 00_intake/
├── 01_analysis/
├── 02_architecture/
│   ├── c4/
│   ├── adr/
│   ├── api/
│   ├── data/
│   └── ai/
├── 03_crosscutting/
│   ├── security/
│   ├── quality/
│   ├── observability/
│   ├── sizing/
│   └── reliability/
├── 04_dev_pack/
├── 05_implementation/
├── 06_verification/
├── 07_release/
└── 08_operations/
```

# Главная модель ролей

`REQUESTER → ANALYST → ARCHITECT → SECURITY/QUALITY/SRE → ANALYST+ARCHITECT GATE → DEVELOPER → CI/QA → ANALYST ACCEPTANCE → ARCHITECT ACCEPTANCE → RELEASE`

# Правило источника истины

- Markdown/YAML/JSON/OpenAPI/diagrams-as-code в Git являются canonical engineering artifacts.
- Сайт визуализирует и маршрутизирует их.
- PDF/Docs используются как представление/сдача, а не как единственный источник истины.
- Любое изменение должно оставлять traceability и evidence.
