# SADEQ / FATHER — Технический проект, первый контрактный пакет TP-001
**Статус:** DESIGN / REVIEW_REQUIRED · **Редакция:** 0.1 · **Дата:** 2026-11-28

## Результат
На основании [ТЗ 0.3](../IDEA_PLUS_REBASELINE_V03/02_TECHNICAL_ASSIGNMENT_GOST_34_602.md) и [ЭП](../SKETCH_PROJECT_V01/README.md) подготовлены первые **строгие JSON Schema Draft 2020-12** и тестовые входы для сквозного случая INC-001. Это **проектные контракты**, а не реализованный сервис или успешно пройденная квалификация.

## Состав
| ID | Материал | Область |
|---|---|---|
| ТП-001 | [Паспорт контрактов и формальная модель входов/выходов](TP-001_INTERFACE_CONTRACTS.md) | FLOW-01/02/06/07, ALG-01/10/11 |
| ТП-002 | [Объект, идемпотентность, события и state reducer](TP-002_OBJECT_EVENT_AND_STATE.md) | ALG-02/03/04/05/06 |
| ТП-003 | [UAG и исполнение с подтверждением](TP-003_ACTION_APPROVAL_AND_RECOVERY.md) | ALG-10/11/12 |
| ТП-004 | [План исполняемых контрактных тестов](TP-004_CONTRACT_TESTS_AND_GATES.md) | FR-NEW-01…04,08…11 |
| JSON schemas | [InboundIncident](contracts/InboundIncidentV1.schema.json) · [ValidatedObservation](contracts/ValidatedObservationV1.schema.json) · [ActionProposal](contracts/ActionProposalV1.schema.json) · [ApprovalDecision](contracts/ApprovalDecisionV1.schema.json) | closed objects, no loose payload |
| fixtures | [valid INC-001](fixtures/inc_001_valid.json) · [unknown nested](fixtures/inc_001_reject_unknown_nested.json) · [forged tenant](fixtures/inc_001_reject_spoofed_tenant.json) | synthetic |
| Code test spec | [pytest contract validation](tests/test_json_contracts.py) | **not executed in GitHub** |
| workflow | [Processing flow](diagrams/TP001_CONTRACT_DATA_FLOW.mmd) | Design |

## Traceability
`FR-NEW-01/02/03/04/08/09/10/11 → ALG-01/02/03/04/05/06/10/11/12 → FLOW-01/02/06/07/08/09 → JSON Schema → TEST → evidence`.
Далее: остальные FLOW-03/04/05/08/09/10, OpenAPI 3.1, реализация FastAPI/PostgreSQL/mock ITSM, controlled approval, security tests, POLYGON. Старый [API v0.1](../PRODUCT_BASELINE_V1/API_DESIGN_V01/README.md) содержит известные слабые места; он не является готовым Contract-Strict API.

## Неизменяемые правила
- `tenant_id`, `principal_id`, `roles` берутся только из серверного доверенного auth-context, **не из request body**.
- Все trust-boundary API закрыты от неизвестных и вложенных полей, с versioned schema.
- `ActionProposal` — данные, а не capability token и не подтверждение права. Подпись/хэш не выдаёт разрешения без актуального auth + policy decision.
- Exactly-once effect — цель при идемпотентном mock ITSM и корректной сверке; **не** гарантия exactly-once network delivery.
- POLYGON не назначает себя сам, не изменяет candidate и не даёт сертификат реального регулятора; все испытания **NOT_RUN**.
- Один корпус синтетических заявок без реальных ПДн, секретов и открытых внешних AI API.

**Требует review:** контрактные схемы не становятся production-ready без настоящего JSON Schema validator, код-ревью, adversarial regression и тестового end-to-end evidence.

## Обязательный усиленный стандарт контрактов (SECURITY BASELINE)
[TP-005 / FATHER-CSSC-001 — Двусторонний Contract-Strict Security Standard](TP-005_CONTRACT_STRICT_SECURITY_STANDARD.md) — **не только JSON-schema**, но 22 поля обязательств/запретов/полномочий/бюджетов, 18 security invariants, OWASP/NIST/OAuth, threat-to-test. [Шаблон каждого контракта](templates/CONTRACT_SECURITY_TEMPLATE.md), [матрица негативных API-тестов](tests/TP005_API_SECURITY_TEST_MATRIX.md). Существующие 4 схемы — **не полноценные утверждённые API-контракты**: response, UAG policy and authorized tool call schemas остаются незаполненными и блокируют заморозку доверенных интерфейсов.
