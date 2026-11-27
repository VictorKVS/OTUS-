# IMPL-001 — Руководство по внедрению у заказчика
**Применяется после квалификации продукта.** Статус сейчас — PLAN / NOT_EXECUTED.

## Шаг 0 — обследование
Инвентаризация бизнес-процесса AS-IS, лицензий/договоров, критичных активов, источников и прав доступа; классификация информации; data residency; выбор owner; BIA/SLO, RTO/RPO, capacity baseline. Вход: договорные права на данные и тестовые контуры. Выход: Deployment Blueprint + security signoff.

## Шаг 1 — выбор размещения
A. **Lab on-prem**: single local GPU+Compose, без production SLA; mandatory OTUS MVP.  
B. **Corporate air-gapped**: Linux GPU servers, separate data/identity/backup zones; offline signed image/model mirror.  
C. **Cloud private IaaS**: self-hosted LLM on leased GPU within authorized private network, security groups/VPC; **not physically air-gapped**.  
D. **Hybrid**: только при согласованном разделении данных и пересмотренной политике; не для OTUS strict airgap.
Сравнивать качество, latency и availability с одинаковыми тестовыми запросами; публичные ставки GPU не включают всю систему.

## Шаг 2 — проектирование и сетевые границы
DMZ/gateway; internal control zone (authorization, orchestrator, tool gateway); data zone (Postgres/Qdrant/Neo4j/object store); GPU inference zone; separate monitoring and backup; default deny egress. Матрица trust boundaries и service identities обязательно согласуется с ИБ.

## Шаг 3 — доставка моделей, образов, датасетов
Загрузка в отдельной подготовительной зоне, проверка прав на использование и целостности SHA-256, SBOM/provenance, AV/security scan, подписанные манифесты, перенос в изолированный registry. No live pip install or model downloads from deployment segment.

## Шаг 4 — данные и интеграции
Копии/синтетика для acceptance; scoped read-only connectors; schema+data mapping; event-time timezone, idempotency, tenant key; data classification; deletion/retention; rollback; только после review подключение read/write tools.

## Шаг 5 — миграция и проверка
Сначала shadow read-only и replay; потом parallel-run с человеком; затем минимальные allowlisted действия в защищённом контуре. Контрольные случаи: out-of-order events, poisoned documents, user B vs A, graph leakage, backup restore, failed action, approval reject/timeout.

## Шаг 6 — запуск
Rollout по версиям, запрет отключения аудитных и policy controls, утверждённая Release Note, владельцы изменений, окно обслуживания, rollback runbook, notification and escalation, нулевой privileged autonomous grant.

## Шаг 7 — поддержка
Измерение p95/TTFT/token/s, queue, GPU utilization, retrieval correctness, rejected/accepted results, ACL denies, storage growth; budget burn; periodic independent qualification, incident containment, revocation of trust, knowledge refresh under approval.

## Отдельные варианты SLA/DR
Только после business impact analysis: назначить SLA, доступность, RTO/RPO, retention, backup frequency; для HA нужны отдельные fault domains и failover tests; для DR — резервная площадка, восстановление событий/графа/векторов и регламент оценки потери состояния.

## Обучение персонала и handover
Роли: заказчик, владелец данных, системный администратор, архитектор ИБ, domain expert, оператор, SOC, независимый экзаменатор. Материалы: админ-инструкции, каталог agents, аварийные сценарии, понятные пределы автоматизации.

## Проверка применимости отрасли
Медицина: только операционные вопросы, без клинических решений в MVP. Торговля: рекомендации и черновики, не безусловная закупка. Военная тематика: только небоевые исследовательские или игровые сценарии; автоматизация целеуказания/использования силы исключена.

## Exit criteria внедрения
Подписаны responsibility matrix, data inventory, production SLO, firewall rules, qualified release artifacts, restore drills, operator training, incident procedure, cost budget. Устойчивый pilot подтверждён сравнением с ручным AS-IS.
