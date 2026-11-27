# SEDA-001 — SADEQ Evidence-Based Engineering Design Algorithm
**Версия:** v1.0 · **Дата:** 2026-11-27 · **Статус:** PROPOSED / NOT_EXECUTED / NOT_QUALIFIED.

**Цель:** стандартизовать архитектурное и программное проектирование SADEQ на основании реальных методов из книг, исследований, документации и собственной проверки, а не на основании необоснованных предположений генеративной модели.

## Состав
- [SEDA алгоритм 12 стадий](01_ENGINEERING_DESIGN_ALGORITHM.md)
- [Библиографический каталог, подтверждённые темы, границы источников](02_BOOKS_AND_PROVENANCE.md)
- [Матрица выбора алгоритмов / паттернов и алгоритм оценки](03_DECISION_MATRIX_AND_ADR.md)
- [Пример применения к B01/B02 — ingest и entity resolution](04_EXAMPLE_B01_B02.md)
- [Инструкция агенту-архитектору / программисту](05_ENGINEER_AGENT_PROTOCOL.md)
- [Трассируемая диаграмма workflow](diagram.mmd)

## Методические основания
Используются **проверенные в библиотеке** фрагменты:
1. James Gough, Daniel Bryant, Matthew Auburn — _Mastering API Architecture_ (C4, ADR, API-first, OpenAPI, contract tests).
2. Suhas Pai — _Designing Large Language Model Applications_ (RAG, retrieval-rewrite-rerank, GraphRAG and its compute/relationship extraction constraints).
3. Antonio Gulli — _Agentic Design Patterns_ (Routing, Parallelization, Reflection, Tool Use, Memory).
4. Chip Huyen — _AI Engineering_ (evidence from inspected excerpt concerning prompt injection and security).
5. _Building Complex Multi-Agent Systems Using Pattern Prompting_ (Choreography, RAG microarchitecture — inspected material).

**Kubernetes Patterns** — назначен инфраструктурной книгой; конкретные паттерны/страницы должны быть перепроверены по точному изданию перед обязательной ссылкой на книгу. Не заявлять, что её главы уже проверены при создании документа.

## Принципы
- Потребность и критерий качества определяются до выбора библиотеки.
- Литературное обоснование + ограничения применимости + альтернативы + эксперимент.
- Каждая граница данных — FATHER Contract-Strict: closed schemas and authorized flow.
- Каждый компонент связывает `BUS/FR → ALG → PAT → CMP → FLOW → API → THR → CTRL → TEST → EVIDENCE → QUAL`.
- Никакие метрики или факты о выполненных тестах не генерируются без evidence.
- Алгоритм выбирается по **обязательным ограничениям сначала** и только затем по сравнительным критериям.
- Весь процесс сохраняет историю ADR, human sign-off и независимые POLYGON tests.

## Related projects
- [HLD eight logical blocks](../HLD_V01/03_BLOCK_CATALOG.md)
- [100 threat scenarios](../SECURE_SDLC_TOP100_V1/TOP_100_THREATS.md)
- [Initial API contract](../API_DESIGN_V01/README.md)
- [FATHER strict API standard](https://github.com/VictorKVS/FATHER_CODEX/blob/main/docs/protocols/CONTRACT_STRICT_API_ALGORITHM_BOUND_DATA_FLOW_V1.md)
