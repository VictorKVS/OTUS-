# THREAT-LIFECYCLE-001 — Единая матрица угроз с IDEA+ до POLYGON и эксплуатации
**Версия:** 1.0 • **Дата:** 27.11.2026 • **Статус:** PROJECT STANDARD / NOT IMPLEMENTED

## Нормативное правило
Матрица угроз SADEQ/FATHER создаётся **при регистрации идеи в IDEA+**, затем сопровождает каждый этап разработки до финальной независимой квалификации POLYGON. Все изменения архитектуры, источников, алгоритмов, схем, моделей, инструментов и инфраструктуры приводят к оценке влияния на угрозы. После выпуска матрица остаётся живой в эксплуатации и закрытии продукта.

В проекте **один канонический реестр угроз**, а не копии матриц у разных команд; локальные threat-models и результаты тестирования ссылаются на неизменные `THR-xxx`. Существующий [реестр 100 угроз](TOP_100_THREATS.md) — начальный каталог сценариев, **не оценка риска конкретного проекта**.

## Фазы накопления и контракты
| Gate | Фаза | Какие сведения должны добавляться | Минимальный артефакт | Ответственный |
|---|---|---|---|---|
| G00 | IDEA+ | первичные активы, бизнес-цель, опасные последствия, запрещённые действия, assumptions, владельцы риска | Initial Threat Register v0; IDEA-THR link | SEC-01 |
| G01 | Бизнес-анализ | процессы, роли, права на данные, BIA/impact, misuse cases | BPMN/AS-IS/TO-BE + BIA + угрозы бизнес-процессам | SEC-01 |
| G02 | C4/DFD и моделирование угроз | границы доверия, entry points, противники, STRIDE, attack paths | C4, DFD, threat model review | SEC-02 |
| G03 | Алгоритмы и информационные контракты | ALG/CMP/FLOW IDs, инварианты, вход/выход, безопасность вычисления и последствия | Algorithm Safety Contract и negative assertions | SEC-02 |
| G04 | API, UAG, полномочия | identity, tenant/ACL, approval, недопустимые поля, TOCTOU, idempotency | OpenAPI, policy contracts, abuse-case tests | SEC-04 |
| G05 | Реализация | найденные уязвимости и ошибки алгоритмов, статический анализ, secure code review | SAST/SCA, unit/property/fuzz results | SEC-03 |
| G06 | Сборка и поставка | зависимости/модели, лицензии, происхождение, подписи, неизменяемость | SBOM, provenance, attestation | SEC-03 |
| G07 | Данные и GraphRAG | trust источников, poisoned documents, ACL в graph/vector/cache, consistency | Corpus versions, dataset tests | SEC-02 / SEC-05 |
| G08 | Обучение и агентные workflow | reward hacking, feedback, self-approval, loop/tool abuse | Evaluation plan, model card, agent trace | SEC-05 |
| G09 | Решения и действия | риск последствий, проверки разрешений, human approval и повторный policy-check | Action/approval trace, policy test evidence | SEC-04 |
| G10 | Финальная POLYGON квалификация | проверка применимости всех threat IDs, выполнение негативных тестов, независимое решение | signed qualification report + residual risk register | SEC-05 |
| G11 | Развёртывание и инфраструктура | K8s/CNI/Pod, GPU/DB, airgap, secrets, backup/DR | infrastructure acceptance tests, failover and egress proof | SEC-03 / SEC-06 |
| G12 | Эксплуатация, изменения, деактивация | обнаруженные инциденты, drift, новые CVE, изменения компонентов, revoked rights, cleanup | monitoring, vulnerability management, incident and decommission evidence | SEC-06 |

**Порядок применения:** фактическая оценка G11-развёртывания должна пройти **до финального эксплуатационного release GO**. Нумерация выше следует существующей Secure SDLC G00–G12, но не означает, что G10 можно финально утвердить без G11; итоговая POLYGON-аттестация обязательно включает уже развёрнутую целевую конфигурацию и результаты G11. В случае изменения окружения — requalification.

## Что именно хранится у угрозы
```yaml
threat_id: THR-016
first_identified_stage: G00
identified_at: null
asset_ids: []
business_requirement_ids: []
component_ids: []
flow_ids: []
algorithm_ids: []
attack_scenario: "..."
impact_description: "..."
likelihood: UNASSESSED
impact_rating: UNASSESSED
inherent_risk: UNASSESSED
controls: []
test_ids: []
test_status: NOT_RUN
evidence_refs: []
residual_risk: UNASSESSED
owner_role: SEC-04
risk_owner: TBD
reviewer_role: SEC-05
disposition: OPEN
change_history: []
last_reviewed_at: null
next_review_trigger: architecture_or_data_change
```
`first_identified_stage` фиксирует **реальный этап первого обнаружения**, не должен автоматически подменяться на G00 для угроз, впервые найденных позже. G00 означает старт **реестра**, а не то, что все 100 угроз известны уже при формулировке идеи.

## Состояния записи
`CANDIDATE → APPLICABILITY_REVIEW → ACCEPTED_FOR_ANALYSIS → CONTROL_DESIGNED → CONTROL_IMPLEMENTED → TESTED → INDEPENDENTLY_REVIEWED → MITIGATED`, либо `NOT_APPLICABLE` (с обоснованием), `RISK_ACCEPTED` (с подписью и сроком), `BLOCKED`, `REOPENED`.
- Нельзя ставить MITIGATED только потому, что «контроль описан» или «исходный код существует».
- Закрытие риска **не удаляет** его историю; создаёт новую запись события и ссылку на доказательства.
- Отметка `NOT_APPLICABLE` требует причины, даты, автора и независимого review.
- Любое появление нового asset/flow/tenant/tool/model/source/permission/algorithm или CVE инициирует impact-analysis и, при необходимости, `REOPENED`.

## Две обязательные проверки матрицы
1. **Coverage completeness:** каждый актив/поток/алгоритм и доверенная граница связан минимум с анализом применимости угроз; каждая применимая угроза имеет CTRL и TEST или мотивированное исключение.
2. **Effectiveness verification:** защита **фактически** сработала при запуске теста в известной версии и окружении; особое внимание безопасности действий и семантике.

## Выпускной контроль
Релизная запись:
`release_sha + tested_deployment_sha + applicable_threats_snapshot_sha + tests_executed + evidence + open_residual_risks + risk_owner_approvals + independent_qualifier_signoff`.

GO запрещён при незакрытом критическом неприемлемом риске, межарендаторной утечке, неподтверждённой политике исполнения, опасной автономной функции или обходе обязательного допуска. Human risk acceptance не является способом снять абсолютные запреты проекта. После инцидента/смены модели/политики/параметров action tool — запрет затронутых действий до переоценки допуска.

## Как сохраняем историю и совместимость
- `TOP_100_THREATS.csv` — стартовый импорт; матрица должна расти сверх 100 сценариев без перенумерации `THR-001...100`.
- Git хранит ревизии реестра, а runtime incidents/test runs — в audit/evidence store с source hash.
- Привязка OTUS: уроки 1–3 (IDEA+), 4–5/9/14 (модель угроз), 11–13 (данные/API), 18–20 (поставка), 21–27 (масштаб/облака/тенантность), 30–31 (governance/API).
- [13 фаз Secure SDLC](SECURE_SDLC_ROADMAP.md) и [шесть ролей ИБ](../../IDEA_PLUS_V0_2/13_SECURITY_ROLES_BUSINESS_ANALYSIS.md).

**Текущий статус:** требование документировано. Отсутствуют принятый live-register, реальные оценки вероятности и влияния, доказательства выполнения 100 тестов и итоговый квалификационный отчёт.
