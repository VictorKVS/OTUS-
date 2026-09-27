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
