# STEP 14 — Lesson 11: Integrations from classic API to AI standards

Статус: **DONE v1**

## Цель

Нормализовать Lesson 11 по visual-first pipeline:

`SCHEMA → VISUAL → OTUS → ARCHITECT PRO → FATHER PRODUCTION → ARTIFACTS → EVIDENCE → TRACEABILITY → MATURITY`

## Фокус

- synchronous API integration;
- asynchronous messaging / broker;
- contracts and versioning;
- reliability and error handling;
- AI-specific integration standards;
- A2A / MCP only where supported by source;
- identity / permissions around tools and external systems;
- observability of integration calls.

## Definition of Done

- фактические материалы Lesson 11 разобраны;
- integration schema создана;
- visual poster создан;
- detail manifest создан;
- production mapping проверен;
- evidence/GAP зафиксированы;
- status/maturity обновлены only by evidence.


## Source-derived result

Источник Lesson 11 подтверждает:
- API Gateway / Message Broker / ETL как варианты интеграции;
- HTTP / SMTP / gRPC;
- asynchronous integration through broker;
- A2A / MCP как современные протоколы;
- ONNX как упомянутый стандарт для AI-компонентов;
- практику отказоустойчивой интеграции с legacy через broker.

Completed practical submission в папке Lesson 11 не найден.

## Production mapping

- `FTH-API-001 · Interface Contract & API Registry`
- `FTH-IGR-001 · Integration Runtime & Messaging`
- `FTH-MCP-001 · MCP Gateway`
- `FTH-GTW-001 · AI Gateway`
- `FTH-OBS-001 · Observability & Audit Plane`
- `FTH-POL-001 · Policy & Security Plane`
- `FTH-MDL-001 · Model Zoo`

## Validation

- status = `materials / M0`;
- 7/7 production IDs resolved;
- 7 artifact/target entries;
- 5 source evidence statements;
- 4 GAP;
- 7 traceability links;
- visual poster present.

## Architect Pro clarification

Источник курса сохраняется буквально, но professional layer разделяет:
- transport protocols / integration patterns;
- MCP/A2A semantics;
- ONNX model portability/exchange artifact.

ONNX не трактуется как transport protocol.

Следующий шаг: **STEP 15 — Lesson 12: Data Architecture for AI Systems**.
