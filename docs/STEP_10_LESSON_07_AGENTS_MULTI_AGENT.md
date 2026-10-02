# STEP 10 — Lesson 07: AI Agents & Multi-Agent Systems

Статус: **DONE v1**

## Цель

Нормализовать Lesson 07 по visual-first pipeline:

`SCHEMA → VISUAL → OTUS → ARCHITECT PRO → FATHER PRODUCTION → ARTIFACTS → EVIDENCE → TRACEABILITY → MATURITY`

## Фокус

- agent architecture;
- tools;
- state / memory;
- planning / routing;
- supervisor / specialist agents;
- handoff;
- multi-agent coordination;
- failure modes;
- human control;
- graph/workflow orchestration.

## Definition of Done

- фактические материалы Lesson 07 разобраны;
- инженерная схема создана;
- visual poster создан;
- detail manifest создан;
- production mapping проверен;
- evidence/GAP зафиксированы;
- status/maturity обновлены только по evidence.


## Source-derived result

Curriculum:
- autonomous agents;
- ReAct / Plan-and-Execute;
- hierarchical / cooperative Multi-Agent patterns;
- travel assistant with Manager → specialist delegation;
- RAG pipeline inside multi-agent process.

Implemented M1.1 evidence:
- LangGraph `StateGraph`;
- `MessagesState`;
- explicit `Command(goto=...)` handoffs;
- Manager / Policy RAG / Flight / Hotel / Budget agents;
- Hybrid RAG with evidence refs;
- retrieval smoke-gate;
- pytest tests;
- OpenAPI continuation;
- CI workflow definition;
- architecture PDF and detailed diagrams.

## Evidence boundary

The lesson source itself says `Статус: не сдано`. Therefore:
- engineering status = `done / M1`;
- OTUS submission status = `not_submitted_in_source`.

A current successful GitHub Actions run was not independently retrieved in this pass, although the workflow definition is present.

## Production mapping

- `FTH-HARNESS-001`
- `FTH-KNW-001`
- `FTH-RAG-001`
- `FTH-WFG-001`
- `FTH-AGT-001`
- `FTH-SUP-001`
- `FTH-EVL-001`

MCP and persistent Memory are intentionally not included as confirmed Lesson 07 runtime capabilities.

## Validation

- 7/7 production IDs resolved;
- 16 artifacts;
- 8 evidence items;
- 6 GAP;
- 8 traceability links;
- visual poster present.

Следующий шаг: **STEP 11 — Lesson 08: Architecture Decision Records**.
