# SADEQ UAA — бизнес-схема агента v0.1
**Дата:** 2026-11-27 · **Статус:** BUSINESS/ALGORITHM DESIGN PROPOSAL · NOT IMPLEMENTED / NOT QUALIFIED.

## Вопрос: «Что конкретно делает агент?»
Получает разрешённое наблюдение о бизнес-объекте → строго валидирует → привязывает к объекту → сохраняет событие → вычисляет состояние → определяет изменения → извлекает проверенные знания → рассчитывает гипотезы/прогноз → формирует предложение → проверяет допустимость и права → получает human approval где необходимо → выполняет разрешённую операцию → сверяет результат → сохраняет evidence/feedback. Любое неразрешённое действие останавливается.

## Схемы и спецификации
- [BUSINESS_SWIMLANES.mmd](BUSINESS_SWIMLANES.mmd) — бизнес-процесс в дорожках роли/системы, с ветвлениями.
- [UAA_PROCESS.mmd](UAA_PROCESS.mmd) — подробный алгоритмический процесс от intake до feedback.
- [01_BUSINESS_PROCESS_AND_ACTORS.md](01_BUSINESS_PROCESS_AND_ACTORS.md) — правила, роли, шаги, события и показатели.
- [02_ALGORITHMS_AND_CONTRACTS.md](02_ALGORITHMS_AND_CONTRACTS.md) — 12 ALG с алгоритмом, пакетами, условиями ошибок и проверками.
- [03_CASE_STOCK_EXAMPLE.md](03_CASE_STOCK_EXAMPLE.md) — воспроизводимый бизнес-кейс на складе с расчётом; данные демонстрационные.
- [04_TRACEABILITY_AND_GATES.md](04_TRACEABILITY_AND_GATES.md) — FR → ALG → B01…B08 → THR → TEST, требования к приёмке.

## Методическая основа, без подмены источника
- *Mastering API Architecture* (Gough/Bryant/Auburn): C4, API-first/OpenAPI, ADR, contract testing.
- *Designing Large Language Model Applications* (Suhas Pai): retrieval-rewrite-rerank, GraphRAG, ограничения graph indexing.
- *Agentic Design Patterns* (Antonio Gulli): routing, tool use, memory, parallelization.
Эти книги объясняют **подходы**, а конкретные ALG-01..ALG-12 являются **проектным синтезом SADEQ**, не прямой цитатой из книги. Для специального алгоритма entity resolution и causal inference необходимо отдельное профильное исследование/проверяемый источник перед квалификацией.

## Главное системное ограничение
B01/B02/B03/B04/B05 — функциональные блоки, а не обязательные отдельные процессы/Pod. Authoritative control outside LLM. Matrix of threats created at IDEA+ and updated at each gate through POLYGON and production.

## Источники внутри проекта
[IDEA+](../../IDEA_PLUS_V0_2/01_IDEA_CONTRACT.md) · [PRD](../02_PRD_REQUIREMENTS_ACCEPTANCE.md) · [HLD](../HLD_V01/README.md) · [SEDA](../ENGINEERING_ALGORITHM_V1/README.md) · [THREAT MATRIX](../SECURE_SDLC_TOP100_V1/THREAT_MATRIX_LIFECYCLE_POLICY.md).

## Детальная теория и проектирование алгоритмов
[05_ALGORITHMS_DETAILED_SPECIFICATION.md](05_ALGORITHMS_DETAILED_SPECIFICATION.md) — все 12 алгоритмов: шаги обработки, границы AI/non-AI, поля входа/выхода, ошибки, тесты, роль безопасности и linkage к SEDA. **Документировано, тесты не запускались.**
