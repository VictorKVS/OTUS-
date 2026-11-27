# SADEQ UAA — IDEA+ / версия v0.2.0 (27.11.2026)

**SADEQ** — Software & Agent Design, Engineering & Qualification.  
**UAA** — Universal Adaptive Agent: универсальное автономное событийно-аналитическое ядро.  
**Статус:** `DESIGN BASELINE / RESEARCH / NOT_IMPLEMENTED / NOT_QUALIFIED`.

## Суть проекта
Система проектирования, разработки, обучения, испытаний и выпуска специализированных агентов на одном проверенном событийно-аналитическом ядре. Агент принимает информацию по множеству каналов, объединяет наблюдения об объектах, ведёт историю событий, вычисляет состояние, анализирует изменения, предлагает прогноз и выполняет только разрешённую реакцию. Доверие — **не свойство промпта**; его получают за независимые тесты и подтверждают при эксплуатации.

## Пакет IDEA+
- [Паспорт и решение о стадиях](01_IDEA_CONTRACT.md)
- [Business Analysis и нотации](02_BUSINESS_ANALYSIS.md)
- [Исследования и feasibility](03_DISCOVERY_FEASIBILITY.md)
- [Архитектура и диаграммы](04_ARCHITECTURE.md)
- [Архитектурные решения ADR](05_ADR_REGISTER.md)
- [Экономика масштабирования](06_ECONOMICS_SCALING.md)
- [Trust / Learning / Continuous Qualification](07_TRUST_QUALIFICATION.md)
- [Отчёт о полноте IDEA+ и дальнейшие шаги](08_IDEA_PLUS_GATE.md)

## Уровни поставки
1. **UAA Core:** ingest → object identity → event store → state → GraphRAG → reasoning/forecast → governed action → feedback.
2. **SADEQ Factory:** конфигурация профиля, контракты, модель доступа, конвейер тестов.
3. **Первый продукт:** Engineer Agent, который проектирует ограниченное изменение следующей версии платформы, но не утверждает собственный релиз.
4. **Демонстрация универсальности:** три разные профиля, 20 спецификаций как целевой эксперимент, а не 20 заявленных готовых агентов.

## Критические ограничения выпускного проекта OTUS
**Только offline/on-prem; никаких внешних LLM API.** Необходимы C4 L1–L4, Deployment, Sequence, ER, ADR, физическое разделение Control/Data plane, LangGraph/state machine, реальный GraphRAG, GPU sizing, observability, права доступа, тест User B на защищённый документ, видео 5–7 минут и нагрузочный отчёт. Сдача не позже чем за восемь дней до защиты.

## Защита интеллектуальной собственности
В публичной версии используются нейтральные имена. Нельзя включать личные пути, приватные репозитории, внутренние имена систем, секреты, защищённые документы. Публикация в персональном GitHub сама по себе не делает владение репозиторием анонимным.

## Статус
Это пакет **проектных гипотез**. Нет результатов запуска, измеренной экономии, испытанного кода или подтверждения технической комиссии. Не выдавать `PROPOSED` за `APPROVED`, `DOCUMENTED` за `VERIFIED`.

## Сквозная программа OTUS 1–31, инфраструктура и экономика (v0.3)

- [10 — Все 31 урок: урок → проектный результат → критерий приёмки → влияние на стоимость](10_OTUS_01_31_TRACEABILITY_MATRIX.md).
- [11 — Реальные российские облачные тарифы на 27.11.2026; CAPEX/OPEX, 40/160/730 ч, модель TCO](11_DEPLOYMENT_CLOUD_FINOPS_RU_2026.md).
- [12 — Варианты размещения (LAB / air-gapped on-prem / облачный IaaS / hybrid), diagram-as-code и варианты масштабирования](12_DEPLOYMENT_SCALING_PATTERNS.md).
- [09 — P1: выборочный аудит существующих компонентов](09_P1_REUSE_AUDIT.md).
- **Excel-калькулятор** `SADEQ_OTUS_31_CLOUD_TCO_2026.xlsx`: предоставляется как отдельный файл в обсуждении проекта; **не загружен в репозиторий**.

### Приоритеты
1. **Реальный финальный MVP — строго offline**. Cloud IaaS — только сравнительная альтернативная архитектура (не air-gapped).
2. Масштабирование разделяется на типы агентов, запросы/GPU, базы данных, tenants, SLA/DR, deployment.
3. Публичные цены — опубликованные значения с URL и датой, не коммерческое предложение или гарантия доступности.
4. До независимых испытаний документы остаются `DESIGN BASELINE / RESEARCH`.

## Продуктовый комплект v1.0 (27 ноября 2026)

Создан отдельный набор **SADEQ Product Baseline v1**: [реестр и входная точка](../PRODUCT_BASELINE_V1/00_PRODUCT_DOCUMENT_REGISTER.md), [Vision и Business Case](../PRODUCT_BASELINE_V1/01_PRODUCT_VISION_AND_BUSINESS_CASE.md), [PRD](../PRODUCT_BASELINE_V1/02_PRD_REQUIREMENTS_ACCEPTANCE.md), [roadmap разработки](../PRODUCT_BASELINE_V1/03_ENGINEERING_AND_RELEASE_ROADMAP.md), [план внедрения](../PRODUCT_BASELINE_V1/04_ENTERPRISE_IMPLEMENTATION_PLAYBOOK.md), [риск/доверие](../PRODUCT_BASELINE_V1/05_RISK_TRUST_QUALITY_REGISTER.md), [экономика и перспективы](../PRODUCT_BASELINE_V1/06_ECONOMICS_COMMERCIALIZATION_AND_FUTURES.md), [сквозная архитектура](../PRODUCT_BASELINE_V1/07_ARCHITECTURE_MODEL_AND_GATES.md), [checklist](../PRODUCT_BASELINE_V1/08_DELIVERY_AND_EVIDENCE_CHECKLIST.md).

**Бизнес-нотации:** [6 ролей](13_SECURITY_ROLES_BUSINESS_ANALYSIS.md), [BPMN](diagrams/security_lifecycle.bpmn), [UML](diagrams/security_use_cases.puml), [DMN](diagrams/security_decision_table.md). Эти модели проектные, требуют formal modeling validation и независимой квалификации.

PDF/DOCX/PPTX и Excel предоставляются отдельным downloadable package в обсуждении, не являются файлами данного GitHub-коммита. Версия документации **не означает реализованный продукт**.
