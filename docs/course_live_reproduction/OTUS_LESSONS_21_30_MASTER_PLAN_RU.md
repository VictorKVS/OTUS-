# OTUS AI Architect — сквозное продолжение уроков 21–30

**Дата:** 2026-11-27  
**Основной проект:** FATHER Architecture Platform; для практики допускается специализированный AI-сервис/OSINT, но единые BUS/REQ/NFR/ADR/CMP/CTRL/TEST/SLO/COST/REL.  
**Статус:** учебная матрица подготовлена по именам каталогов OTUS- и COURSE_REGISTRY.yaml / ARCHITECTURE_ROADMAP.md; уроки 21–30 **не считаются выполненными** без собственных evidence.

## Режим

- **M1:** изучить исходник урока, составить краткое инженерное решение, схему, контракты, критерии приёмки.
- **M2:** сравнить альтернативы; расчёты/обоснования; подтвердить зависимости и официальные источники.
- **M3:** реализовать локальную/песочничную лабораторию и исполнить тесты, где возможно.
- Kubernetes трек — **часть основного курса**, не независимый проект; интеграция IaC, GitOps, K8s и AI-сервисов.
- Для всего курса: `BUS → REQ/NFR → RISK → ADR → CMP → CTRL → TEST → SLO → COST → REL`.
- Не присваивать PASS без результатов тестирования. Сроки, RPS, p95 и деньги не подменять догадками.

## Точные темы и проектные поставки

| № | Тема из каталога OTUS- | Минимальный артефакт FATHER | Независимое подтверждение |
|---|---|---|---|
| 21 | HA и DR | HA/DR topology, RTO/RPO, replication + failover ADR | сценарии отказов, restore drill, измерения RTO/RPO |
| 22 | Serverless vs Kubernetes | сравнительная матрица размещения: latency, cold start, operations, control, TCO | нагрузочный профиль, costing, контракты workloads |
| 23 | EDA для AI | схема event producers / broker / consumers, envelopes, idempotency | replay, out-of-order, retries, DLQ, schema version |
| 24 | High-Load и Low-Latency inference (ДЗ) | capacity model, cache/routing, batching, scale, KEDA/HPA | нагрузочный тест, p95/p99 и стоимость на workload |
| 25 | Гибридная и мультиоблачная архитектура | placement policy, data residency, routing/failover, identity | simulated provider outage, cost, data controls |
| 26 | Multi-tenancy в AI SaaS | tenant isolation, RBAC/quotas, model/data separation | negative cross-tenant access tests |
| 27 | Federated Learning / Privacy-Preserving | threat model, data flow, FL feasibility and privacy controls | privacy/security assessment; limitations documented |
| 28 | FinOps | FinOps cost allocation, cost-per-qualified-answer, budgets | reproducible tariff assumptions and sensitivity analysis |
| 29 | Технологический радар и эволюция | radar adopt/trial/assess/hold + migration ADRs | time-bound evidence and revisit gates |
| 30 | Ethical AI by Design + Governance (ДЗ) | model card, governance controls, oversight, audit matrix | evidence of control execution, independent audit |

**Граница:** названия подтверждены каталогами репозитория; проектные артефакты выше — **наше предложенное применение** и требуют сверки с полными учебными файлами конкретных занятий.

## Gate G6 — уроки 21–27

Проверить: восстановление, выбор инфраструктуры, события, масштабирование инференса, гибридное размещение, multi-tenancy и privacy. Не считать архитектуру надёжной только по C4-диаграмме: требуются измеримые тесты отказа.

## Gate G7 — уроки 28–30 (+31 остаётся за пределами текущего запроса)

Подтвердить TCO/FinOps, технологический радар и AI-governance. В COURSE_REGISTRY.yaml этап G7 официально включает также урок 31 «API как продукт», но здесь ограничиваемся уроком 30.

## На чём продолжаем

Урок 20: постановка `10,000 RPS`, `latency <200ms` не должна механически применяться к полному LLM-ответу. Разделить:
- быстрые deterministic/cache API: p95 <200 ms — гипотеза SLO, требует load testing;
- генерация LLM: отдельно TTFT, total completion latency, throughput/tokens/s и quality.
Решение урока 21 наследует эти workload classes и вводит HA/DR так, чтобы независимые отказы не разрушали сервис.

## Учебный алгоритм каждого занятия

1. Прочитать точный исходный материал OTUS.
2. Словарь и простое объяснение; зачем нужен каждый паттерн.
3. Архитектурная задача заказчика и NFR/ограничения.
4. Три варианта решения с ADR, data/security/cost contracts.
5. Расчёты, Python/K8s/GitOps лаборатория, где применимо.
6. Негативные тесты, измерения и evidence.
7. Сайт, готовый ответ преподавателю, перечень открытых рисков.

**Текущий следующий шаг:** [Урок 21 HA/DR](LESSON_21_HA_DR_ARCHITECT_NOTES_RU.md).
