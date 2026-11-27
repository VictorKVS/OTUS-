# IDEA+ REBASELINE V0.3 · SADEQ Enterprise Operations Copilot
**Дата:** 2026-11-27 · **Status:** DRAFT / PROPOSED · **Goal:** shift from broad agent factory to one demonstrable safe corporate AI agent without abandoning universal architecture.

- [08 Мировые и российские аналоги / проверяемые KPI и конкурирующие решения](08_WORLD_ANALOGS_AND_BENCHMARKS.md) — справка рядом с ТЗ, ссылки на первоисточники; достижения аналогов не приписываются SADEQ.
## Start here

- [05 Целевое корпоративное размещение агента (Z0–Z7)](05_ENTERPRISE_DEPLOYMENT_HORIZON.md)
- [06 Корпус знаний, алгоритмы и учебная программа L0–L8](06_AGENT_KNOWLEDGE_CURRICULUM.md)
- [07 План испытаний и независимая квалификация Q00–Q11](07_AGENT_TRAINING_AND_QUALIFICATION.md)
- [Схема корпоративного включения и квалификации](diagrams/SADEQ_CORPORATE_LANDING_AND_QUALIFICATION.mmd)

- [01 IDEA+ — паспорт новой идеи](01_IDEA_PLUS_REBASELINE.md)
- [02 Техническое задание по ГОСТ 34.602-2020](02_TECHNICAL_ASSIGNMENT_GOST_34_602.md)
- [03 Матрица FR-NEW-01…20 и приёмки](03_REQUIREMENTS_ACCEPTANCE_MATRIX.md)
- [04 Impact старого IDEA+/PRD на новую редакцию](04_CHANGE_IMPACT_V02_TO_V03.md)

## Architecture contract
This is a **new version**; old documents retained and not overwritten. Traces to [Market research](../MARKET_DRIVEN_MVP_2026_11/README.md), [HLD](../PRODUCT_BASELINE_V1/HLD_V01/README.md), [12 algorithms](../PRODUCT_BASELINE_V1/BUSINESS_AGENT_V01/05_ALGORITHMS_DETAILED_SPECIFICATION.md), [SEDA](../PRODUCT_BASELINE_V1/ENGINEERING_ALGORITHM_V1/README.md), [GOST documentation](../PRODUCT_BASELINE_V1/GOST_ENGINEERING_DOC_SYSTEM_V01/README.md) and [OTUS lessons](../IDEA_PLUS_V0_2/10_OTUS_01_31_TRACEABILITY_MATRIX.md).

## Important trade-off
P0 = actual running local service desk assistant (RAG, tool, human approval, security, evidence). P1 = OTUS full qualification (GraphRAG, profiles, Kubernetes, TCO). P2 = further research factory/forecast/tuning. **P1 still mandatory for OTUS target**, not deleted from product ambition.

## Formality
ГОСТ 34.602 layout used for content; no title block signatures, formal contract numbering or actual customer acceptance. PDF/DOCX typeset derivative does not by itself prove certification/compliance. No deployed product/test evidence asserted.

## Visual architecture / figures
[IDEA+ with 11 embedded figures](01_IDEA_PLUS_REBASELINE.md) · [Business flow](diagrams/SADEQ_BUSINESS_FLOW_V03.svg) · [C4](diagrams/VIS-03_C4_CONTEXT_CONTAINER.svg) · [Zero Trust / UAG](diagrams/VIS-04_ZERO_TRUST_UAG.svg) · [RAG](diagrams/VIS-05_RAG_GRAPHRAG.svg) · [Traceability](diagrams/VIS-07_TRACEABILITY_GATES.svg). All SVG images are vector source, DESIGN, NOT QUALIFIED; official BPMN/ГОСТ deliverables separate.

## Эскизный проект и операционная концепция
[ЭП V0.1: ConOps, UC, HLD, ADR, traceability](../SKETCH_PROJECT_V01/README.md) — первая рабочая редакция, не утверждено заказчиком, испытания NOT_RUN.
