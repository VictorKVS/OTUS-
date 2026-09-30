# FATHER Architect OS — дневник разработки

## Правила ведения

Дневник append-only по смыслу: старые записи не переписываются для создания более красивой истории. Исправления и развитие оформляются новой записью.

Каждая запись содержит:
- дата;
- ветка/контекст;
- STEP;
- цель;
- сделано;
- evidence;
- что стоит улучшить;
- как улучшить;
- приоритет;
- GAP/риски;
- следующий STEP.

---

## 2026-09-27 — восстановление сайта и фиксация боевой линии

**Ветка:** `feature/otus-homework-site`  
**Контекст:** локальный корень `G:\1\OTUS`, repository `VictorKVS/OTUS-`.

### Что подтверждено

- сайт расположен в `site/`;
- рабочая ветка сайта — `feature/otus-homework-site`;
- сайт синхронизирован до актуального remote состояния;
- существуют `index.html`, `app.js`, `styles.css`, `README.md`;
- Lesson 01 имеет отдельные страницы `lesson-01.html` и `lesson-01-intake.html`;
- первый урок уже реализует два слоя: учебный материал + экспертное расширение;
- Architect Intake Pack содержит расширенный реестр входов архитектора.

### Архитектурное решение

Сайт развивается не как каталог ДЗ, а как **FATHER Architect OS / OTUS Architecture Cockpit** с тремя слоями:

`OTUS Curriculum → Architect Pro → FATHER Production`.

Для каждого шага обязательна структура:

`Схема → Визуал → Смысл → Артефакты → Проверки → FATHER Mapping → Зрелость`.

### Новая capability-ось

В боевой план включены:
Harness, Context Engineering, Prompt Optimization, Loop/Graph Engineering, MCP, Tool Use, Agentic/Multi-Agent, RAG 2.0, Memory, Vector DB, Fine-tuning/Distillation, Evaluation, Guardrails, Observability, Synthetic Data, AI Gateways, Cost Optimization.

Добавлены production-блоки, которых недостаточно в исходном capability checklist:
IAM, secrets, policy, governance/provenance, human review, artifact registry, CI/CD, deployment/rollback, HA/DR, threat modeling, audit, sizing/capacity, incident lifecycle.

### Что стоит улучшить

1. Реестр уроков пока жёстко хранится в `site/app.js`.
2. Нет единого машинно-читаемого capability/lesson manifest.
3. Визуальный стандарт ещё не применён ко всем страницам.
4. Нет master map всей платформы.
5. Статусы многих уроков отражают наличие материалов, а не полную production зрелость.

### Как улучшить

- выполнить STEP 00 как нормативный документ;
- перейти к STEP 01: master architecture map;
- затем вынести данные в manifest;
- после этого сделать универсальный lesson template;
- только затем масштабировать на уроки 02–31.

### Приоритет

**P0:** STEP 00 → STEP 01 → STEP 02 → STEP 03.  
**P1:** нормализация Lesson 01.  
**P2:** последовательное расширение Lessons 02–31.

### GAP / риски

- локальное рабочее дерево содержит посторонние type-changed и untracked файлы; не смешивать их с сайтом;
- `_PRIVATE_BOOK_CORPUS/` не должен случайно попасть в публичный репозиторий;
- визуалы должны иметь текстовый/семантический эквивалент, чтобы смысл не зависел только от цвета/изображения.

### Следующий шаг

**STEP 00 — формализация нотации и визуального языка.**

---

## 2026-09-27 — STEP 00

**Статус:** DONE.

### Сделано

Создан стандарт:
`docs/STEP_00_NOTATION_AND_VISUAL_LANGUAGE.md`.

Зафиксированы:
- типы сущностей;
- типы связей;
- M0–M3;
- трехслойная модель;
- AI Capability Map;
- обязательные production capabilities;
- мастер-схема;
- Definition of Done страницы.

### Evidence

Документ STEP 00 в текущей ветке и ссылки из roadmap/site README после обновления.

### Что стоит улучшить

Проверить нотацию на реальной master map; при конфликте обозначений выпускать v1.1, не менять молча смысл существующих кодов.

### Следующий шаг

**STEP 01 — Master Architecture Map.**


---

## 2026-09-27 — STEP 01 started

**Статус:** IN PROGRESS.

### Сделано

- создан `docs/STEP_01_MASTER_ARCHITECTURE_MAP.md`;
- сформирована первая master schema;
- сформирована сквозная traceability schema;
- capabilities сгруппированы по доменам;
- создана первичная матрица capability ↔ OTUS lessons;
- в roadmap и site README закреплён visual-first стандарт.

### Evidence

- `docs/STEP_01_MASTER_ARCHITECTURE_MAP.md`
- `docs/STEP_00_NOTATION_AND_VISUAL_LANGUAGE.md`
- `ARCHITECTURE_ROADMAP.md`
- `site/README.md`

### Что стоит улучшить

STEP 01 пока не закрыт: отсутствует отдельный визуальный poster и machine-readable capability manifest.

### Как улучшить

Следующим проходом сделать визуальный poster строго по master schema, затем перенести capability mapping в JSON/YAML для сайта.

### Приоритет

**P0.**

### Следующий шаг

Завершить STEP 01: visual poster + component IDs + capability manifest.


---

## 2026-09-27 — STEP 01 completed

**Статус:** DONE v1.

### Сделано

- опубликована страница `site/step-01-master-map.html`;
- создан визуальный poster `site/assets/step-01-master-architecture.svg`;
- создан machine-readable `site/data/capabilities.json`;
- введены component IDs для ключевых production domains;
- capability ↔ lesson mapping включён в manifest;
- Master Map добавляется в основную навигацию Cockpit.

### Evidence

- `site/step-01-master-map.html`
- `site/assets/step-01-master-architecture.svg`
- `site/data/capabilities.json`
- `docs/STEP_01_MASTER_ARCHITECTURE_MAP.md`

### Что стоит улучшить

- назначить owners для capability domains;
- довести mapping до evidence-level;
- добавить автоматическую валидацию manifest/IDs.

### Как улучшить

В M2 добавить owners/reviewers и JSON Schema/CI validation.

### Приоритет

**P1 после STEP 02–03.**

### Следующий шаг

**STEP 02 — Machine-readable Course Manifest.**


---

## 2026-09-27 — STEP 02 completed

**Статус:** DONE v1.

### Сделано

- создан `site/data/course-manifest.json`;
- 31 урок и 7 gates вынесены в manifest;
- каждый урок связан с maturity и FATHER capability IDs;
- `site/app.js` переведён на загрузку manifest;
- создан визуальный poster `site/assets/step-02-course-manifest.svg`;
- создана страница `site/step-02-course-manifest.html`.

### Validation

- lessons = 31;
- gates = 7;
- gate/maturity/production mapping присутствует у каждого урока;
- hardcoded lesson registry отсутствует.

### Что стоит улучшить

- добавить JSON Schema и CI validation;
- позже получать часть статусов автоматически из evidence/CI;
- отделить lesson-specific detail data от общего manifest.

### Следующий шаг

**STEP 03 — Universal Lesson Template.**

---

## 2026-09-27 — STEP 03 started

**Статус:** IN PROGRESS.

### Цель

Создать единый visual-first шаблон для всех 31 уроков.

### Первый контрольный пример

Lesson 01: сохранить Architect Intake Pack, но привести страницу к общей структуре `Schema → Visual → OTUS → Architect Pro → FATHER Production → Evidence → Maturity`.


---

## 2026-09-28 — STEP 03 completed

**Статус:** DONE v1.

### Сделано

- создан reusable lesson shell `site/lesson-template.html`;
- создан manifest-driven runtime `site/lesson-template.js`;
- создан общий responsive layout `site/lesson-template.css`;
- создан detail-contract `site/data/lesson-detail-template.json`;
- создан visual poster `site/assets/step-03-universal-lesson-template.svg`;
- создана отдельная страница STEP 03;
- fallback показывает GAP вместо выдуманных данных.

### Validation

- course facts загружаются из manifests;
- layout отделён от lesson-specific content;
- capability IDs подтягиваются из production mapping;
- отсутствующий detail manifest не ломает страницу;
- структура Schema → Visual → OTUS → Architect Pro → FATHER → Evidence → Maturity соблюдается.

### Что стоит улучшить

- добавить schema validation для detail manifests;
- добавить prev/next lesson navigation;
- добавить автоматический visual registry.

### Следующий шаг

**STEP 04 — Lesson 01 normalization.**

---

## 2026-09-28 — STEP 04 started

**Статус:** IN PROGRESS.

### Цель

Перевести Lesson 01 на универсальный visual-first template без потери Architect Intake Pack, словаря и существующих evidence.


---

## 2026-09-28 — STEP 04 completed

**Статус:** DONE v1.

### Сделано

- создан `site/data/lesson-details/01.json`;
- создан visual poster `site/assets/lesson-01-architect-intake.svg`;
- Lesson 01 подключён к `lesson-template.html?id=1`;
- сохранены legacy expert/intake pages;
- добавлены `FTH-INT-001` и `FTH-REQ-001`;
- Lesson 01 переведён в `draft / M1`;
- universal runtime расширен templates / red flags / runtime notes.

### Validation

- 3/3 capability IDs существуют;
- 13 artifacts;
- 4 evidence;
- 3 GAP;
- schema и poster присутствуют.

### Архитектурный вывод

Context Builder не владеет требованиями. Intake/Requirements/Traceability выделены в отдельный production-domain.

### Следующий шаг

**STEP 05 — Lesson 02: проектирование и оценка, риски и смета.**

---

## 2026-09-28 — STEP 05 started

**Статус:** IN PROGRESS.

### Цель

Разобрать Lesson 02 по фактическим материалам и построить schema + visual + professional + production mapping.


---

## 2026-09-28 — STEP 05 completed

**Статус:** DONE v1.

### Сделано

- создан `site/data/lesson-details/02.json`;
- создан `site/assets/lesson-02-estimation-risk-cost.svg`;
- Lesson 02 подключён к universal template;
- добавлены `FTH-EST-001` и `FTH-RSK-001`;
- Lesson 02 = `draft / M1`.

### Source-derived scope

Нормализованы: SRS/NFR, Analogous/Parametric/PERT/Bottom-Up, WBS, Risk Register, Change Request, TCO, unit economics, effort estimation.

### Validation

- 4/4 production IDs;
- 11 artifacts;
- 4 evidence;
- 3 GAP.

### Следующий шаг

**STEP 06 — Lesson 03: PoC → Production.**

---

## 2026-09-28 — STEP 06 started

**Статус:** IN PROGRESS.


---

## 2026-09-30 — STEP 06 completed

**Статус:** DONE v1.

### Сделано

- создан `site/data/lesson-details/03.json`;
- создан `site/assets/lesson-03-poc-to-production.svg`;
- Lesson 03 подключён к `lesson-template.html?id=3`;
- добавлен `FTH-VAL-001 · Value Delivery & Stage Gate Service`;
- Lesson 03 = `draft / M1`.

### Source-derived scope

Из материалов подтверждены: Demo, PoC, MVP, Production, staged delivery, contract strategy, Roadmap с DoD, risk matrix и количественный risk register.

### Validation

- 5/5 production IDs существуют;
- 10 artifacts;
- 4 evidence;
- 4 GAP;
- 7 traceability links;
- visual poster присутствует.

### Важное ограничение

Исходный текст Lesson 03 содержит статус `не сдано`. Нормализация сайта не считается подтверждением сдачи учебного ДЗ.

### Следующий шаг

**STEP 07 — Lesson 04: HLD / C4 Model.**

---

## 2026-09-30 — STEP 07 started

**Статус:** IN PROGRESS.

### Цель

Нормализовать HLD и C4 как следующий слой после G1: от бизнес-контекста и требований к границам системы, контейнерам, внешним акторам и архитектурным решениям.


---

## 2026-09-30 — STEP 07 completed

**Статус:** DONE v1.

### Сделано

- создан `site/data/lesson-details/04.json`;
- создан `site/assets/lesson-04-hld-c4.svg`;
- Lesson 04 подключён к universal template;
- добавлен `FTH-ARC-001 · Architecture Model & View Registry`;
- Lesson 04 = `draft / M1`.

### Source-derived distinction

OTUS требует C1/C2. Существующий Structurizr DSL дополнительно содержит C3, Deployment и AI-specific actors — это отделено как Architect Pro.

### Validation

- 2/2 production IDs;
- 9 artifacts;
- 5 evidence;
- 4 GAP;
- 6 traceability links.

### Следующий шаг

**STEP 08 — Lesson 05: LLD, компоненты и взаимодействия.**

---

## 2026-09-30 — STEP 08 started

**Статус:** IN PROGRESS.


---

## 2026-09-30 — STEP 08 completed

**Статус:** DONE v1.

### Сделано

- создан `site/data/lesson-details/05.json`;
- создан `site/assets/lesson-05-lld-contracts.svg`;
- Lesson 05 подключён к universal template;
- добавлен `FTH-API-001 · Interface Contract & API Registry`;
- Lesson 05 сохранён как `done / M1`.

### Validation

- 3/3 production IDs;
- 14 artifacts;
- 6 evidence;
- 3 GAP;
- 7 traceability links.

### Архитектурный вывод

C3, Sequence и OpenAPI должны описывать один и тот же контракт взаимодействия. API contract становится first-class versioned artifact.

### Следующий шаг

**STEP 09 — Lesson 06: RAG patterns.**

---

## 2026-09-30 — STEP 09 started

**Статус:** IN PROGRESS.


---

## 2026-09-30 — STEP 09 completed

**Статус:** DONE v1.

### Сделано

- создан `site/data/lesson-details/06.json`;
- создан `site/assets/lesson-06-rag-patterns.svg`;
- Lesson 06 подключён к universal template;
- добавлен `FTH-KGR-001 · Knowledge Graph Service`;
- Memory Layer удалён из прямого Lesson 06 mapping;
- Lesson 06 = `draft / M1`.

### Validation

- 5/5 production IDs;
- 8 artifacts;
- 7 evidence;
- 5 GAP;
- 8 traceability links.

### Важный GAP

Notebook содержит RAG/hybrid/rerank code, но не имеет сохранённых execution outputs. Папка `lesson-06-c4-model` не относится к RAG и должна быть перенесена/переименована.

### Следующий шаг

**STEP 10 — Lesson 07: AI Agents & Multi-Agent Systems.**

---

## 2026-09-30 — STEP 10 started

**Статус:** IN PROGRESS.


---

## 2026-09-30 — STEP 10 completed

**Статус:** DONE v1.

### Сделано

- создан `site/data/lesson-details/07.json`;
- создан `site/assets/lesson-07-multi-agent.svg`;
- Lesson 07 подключён к universal template;
- production mapping очищен от неподтверждённых MCP / persistent Memory;
- добавлена manifest-driven навигация Previous / Course Map / Next;
- введён отдельный `curriculum.submission_status`;
- Lesson 03 и Lesson 07 помечены `not_submitted_in_source`;
- Lesson 07 сохранён как engineering `done / M1`.

### Validation

- 7/7 production IDs;
- 16 artifacts;
- 8 evidence;
- 6 GAP;
- 8 traceability links.

### Важное правило

Engineering `done` ≠ OTUS `accepted`. Сайт теперь показывает эти статусы отдельно.

### Следующий шаг

**STEP 11 — Lesson 08: Architecture Decision Records.**

---

## 2026-09-30 — STEP 11 started

**Статус:** IN PROGRESS.


---

## 2026-09-30 — STEP 11 completed

**Статус:** DONE v1.

### Сделано

- создан `site/data/lesson-details/08.json`;
- создан `site/assets/lesson-08-adr-lifecycle.svg`;
- добавлен `FTH-ADR-001 · Architecture Decision Registry`;
- Lesson 08 = engineering `done / M1`.

### Validation

- 6/6 production IDs;
- 8 artifacts;
- 7 evidence;
- 5 GAP;
- 8 traceability links.

### Архитектурный вывод

Accepted ADR не переписывается задним числом. Изменение условий ведёт к review и новому superseding ADR.

### Следующий шаг

**STEP 12 — Lesson 09: Architecture Verification / CTO Challenge.**

---

## 2026-09-30 — STEP 12 started

**Статус:** IN PROGRESS.


---

## 2026-09-30 — STEP 12 completed

**Статус:** DONE v1.

### Сделано

- создан `site/data/lesson-details/09.json`;
- создан `site/assets/lesson-09-architecture-verification.svg`;
- добавлен `FTH-REV-001 · Architecture Review & Challenge Service`;
- Lesson 09 сохранён как `review / M1`;
- curriculum status = `not_submitted_in_source`.

### Validation

- 6/6 production IDs;
- 12 artifacts;
- 6 evidence;
- 6 GAP;
- 8 traceability links.

### Ключевой вывод

Подготовленный pitch/ADR не равен завершённой CTO Challenge session. Для закрытия G3 требуется review evidence и разрешение critical findings.

### Следующий шаг

**STEP 13 — Lesson 10: Architecture Governance / Technical Debt.**

---

## 2026-09-30 — STEP 13 started

**Статус:** IN PROGRESS.


---

## 2026-09-30 — STEP 13 completed

**Статус:** DONE v1.

### Сделано

- создан `site/data/lesson-details/10.json`;
- создан `site/assets/lesson-10-governance-tech-debt.svg`;
- добавлен `FTH-GOV-001 · Architecture Governance & Technical Debt Service`;
- Lesson 10 подключён к universal template.

### Evidence boundary

В папке урока обнаружен только source lesson text. Завершённый PR-review / Debt Register отсутствует.

Поэтому статус честно сохранён как `materials / M0`.

### Validation

- 5/5 production IDs;
- 6 artifact/target entries;
- 4 source evidence statements;
- 5 GAP;
- 7 traceability links.

### Milestone

Lessons **01–10** теперь имеют единый visual-first representation:
Schema → Visual → OTUS → Architect Pro → FATHER Production → Evidence → Maturity.

### Следующий шаг

**STEP 14 — Lesson 11: Integrations from classic API to AI standards.**

---

## 2026-09-30 — STEP 14 started

**Статус:** IN PROGRESS.
