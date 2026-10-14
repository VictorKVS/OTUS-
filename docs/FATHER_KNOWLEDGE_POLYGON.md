# FATHER Knowledge Polygon · Projects × Phases 0–20

## Цель

Все проекты экосистемы проходят через одну и ту же инженерную шкалу 0–20. Это превращает портфель проектов в **полигон знаний**: один и тот же архитектурный принцип проверяется на разных доменах, а лучший подтверждённый механизм возвращается в FATHER как reusable block/pattern.

```text
PROJECT
  ↓
PHASE 0 … PHASE 20
  ↓
EVIDENCE
  ↓
LESSONS LEARNED
  ↓
REUSABLE BLOCK / PATTERN
  ↓
FATHER BLOCK REGISTRY
  ↓
NEXT PROJECT
```

## Не 23 независимых домашних задания

Проект остаётся самим собой. Фазы задают одинаковые вопросы:

- что строим и зачем;
- какие требования/риски;
- какая архитектура;
- как проверяем;
- как защищаем;
- как наблюдаем;
- как считаем ресурсы;
- как поставляем;
- как выпускаем и откатываем.

Если фаза неприменима, ставится `N/A + rationale`, а не искусственная реализация.

## Канонические фазы

| # | Код | Результат |
|---:|---|---|
| 0 | `IDEA` | Замысел / intake / project charter |
| 1 | `BUSINESS` | Бизнес-контекст, stakeholders, value |
| 2 | `REQ_RISK` | REQ/NFR, риски, оценка |
| 3 | `VALUE` | PoC→MVP→Production, stage gates |
| 4 | `HLD` | C4 C1/C2, HLD |
| 5 | `LLD` | C3, sequence, OpenAPI/contracts |
| 6 | `RAG` | Knowledge/RAG architecture |
| 7 | `AGENT` | Agent/MAS workflow |
| 8 | `ADR` | Architecture Decision Records |
| 9 | `REVIEW` | Architecture verification / CTO challenge |
| 10 | `GOV` | Governance / tech debt |
| 11 | `INTEGRATION` | API/events/MCP/tools |
| 12 | `DATA` | Data architecture / lineage / retention |
| 13 | `EVAL` | Evaluation / golden sets / A-B |
| 14 | `SECURITY` | Threat model / controls / guardrails |
| 15 | `OBS` | Observability / SLO / alerts |
| 16 | `SIZING` | CPU/RAM/storage/vector DB sizing |
| 17 | `INFERENCE` | LLM/GPU inference sizing |
| 18 | `DELIVERY` | IaC / CI/CD / DevSecOps |
| 19 | `MLOPS` | Model/data/index lifecycle |
| 20 | `PROD` | Canary / GitOps / rollback |

## Портфель полигона

| ID | Проект | Домен | Статус | Роль в полигоне |
|---|---|---|---|---|
| KPOL-001 | FATHER / Architect OS | core-platform | ACTIVE | Главный архитектурный конвейер и место сборки знаний. |
| KPOL-002 | FATHER Engineering Competency Lab | education-lab | ACTIVE | Полигон инженерных компетенций и практических кейсов. |
| KPOL-003 | Knowledge Core / Knowledge Factory | knowledge | ACTIVE | Нормализация, provenance, KB/RAG, knowledge lifecycle. |
| KPOL-004 | Automation Control Center | automation | ACTIVE | Автоматизация исполнения и операционный контроль. |
| KPOL-005 | OSINT_deepseek | osint | ACTIVE_NO_TOUCH | OSINT-агент и поставщик evidence для Knowledge Factory. |
| KPOL-006 | SecGraph | security | ACTIVE | Threat modeling + OSINT + pentest + document engine. |
| KPOL-007 | UAG / Universal Agent | agents | ACTIVE | Универсальный агентный runtime и supervisor patterns. |
| KPOL-008 | Model Zoo / Agent Zoo | platform-ai | ACTIVE | Реестр моделей/агентов, маршрутизация и совместимость. |
| KPOL-009 | Alina Knowledge Worker / Analyst | knowledge-agent | ACTIVE | Аналитик знаний: ingestion → understanding → graph → KB. |
| KPOL-010 | Makar Frontend Factory | frontend | ACTIVE | Frontend/creative engineering и reusable visual systems. |
| KPOL-011 | BOOKCRAFT / Creative Production Studio | creative | ACTIVE | Configuration-driven creative production engine. |
| KPOL-012 | MindForge Studio | visual-ai | ACTIVE | Visual AI pipeline, generation, consistency and QC. |
| KPOL-013 | father-quant-lab | quant | ACTIVE | Количественные эксперименты и модели. |
| KPOL-014 | father-media-lab | media | ACTIVE | Медиа-пайплайны и мультимодальные эксперименты. |
| KPOL-015 | Local LLMs | local-llm | ACTIVE | Локальные модели, inference, benchmarking and serving. |
| KPOL-016 | Vibe Coding Router | dev | ACTIVE | Интеграции, runtime UI/API, provider routing и учебные DZ. |
| KPOL-017 | DZ18 External Service / Image Lab | integration | ACTIVE | Полигон внешних AI-сервисов, media/persona/runtime integration. |
| KPOL-018 | CyberED / Security KB | security-education | ACTIVE | ИБ-инженерия, аудит, regulatory knowledge and pentest tracks. |
| KPOL-019 | Regulatory Twin / Alina-lawyer | regulatory | DESIGN | Нормативные требования, применимость, ответственность, controls. |
| KPOL-020 | DevSecOps Factory | devsecops | DESIGN | Reusable delivery-security blocks and release gates. |
| KPOL-021 | Story / Narrative Engine | narrative | ACTIVE | Canon, state, continuity, structured story production. |
| KPOL-022 | AI Product Architect | product | DESIGN | Product/architecture synthesis and decision support. |
| KPOL-023 | PX00 / FATHER legacy core | core-legacy | ACTIVE_NO_TOUCH | Исторический/активный контур; только картирование, без изменений. |

> `ACTIVE_NO_TOUCH`: проект картируется в матрице, но его репозиторий/код не изменяется без отдельного решения.

## Как работаем с каждым проектом

Для каждой клетки `PROJECT × PHASE` храним:

| Поле | Смысл |
|---|---|
| applicability | REQUIRED / OPTIONAL / N/A |
| status | NOT_ASSESSED / DESIGN / LAB / VALIDATED / PROD |
| artifacts | ссылки на реальные документы/код |
| evidence | тесты, benchmark, screenshots, run logs |
| numbers | COURSE / SOURCE / LAB / PROD provenance |
| gaps | чего не хватает |
| reusable_output | какой block/pattern можно вынести |
| feeds_father | куда возвращается знание в FATHER |

## Главный эффект

Например, Canary не изучается один раз в учебном проекте:

```text
SAIKA Canary
BOOKCRAFT release
ALINA release
OSINT release
CyberED release
Local LLM release
        ↓
COMPARE
        ↓
CANARY / RELEASE PATTERN v2
        ↓
FATHER BLOCK REGISTRY
```

То же для RAG, security, observability, A/B, sizing, model routing, knowledge ingestion, frontend, CI/CD и т.д.

## Порядок углубления

1. SAIKA остаётся **эталонным reference project 0–20**.
2. Параллельно заводится матрица всех проектов.
3. На каждой фазе сначала отрабатывается эталон.
4. Затем тот же gate прогоняется по релевантным проектам.
5. Различия фиксируются как domain variants.
6. Общая часть выносится в reusable block.
7. Block получает contract, config, tests, metrics, version and evidence.

Это превращает курс в системное накопление инженерного капитала, а не в набор одноразовых работ.
