# FATHER Architect OS — план строительства от STEP 00

## Принцип

Разработка идёт последовательными шагами. Каждый шаг проходит одинаковый цикл:

`Notation/Schema → Visual → Content → Artifacts → Tests/Evidence → FATHER Mapping → Maturity → Journal`

Нельзя считать шаг закрытым только по наличию текста или красивой картинки.

## STEP 00 — Visual & Notation Standard

**Цель:** зафиксировать единый язык сайта и архитектуры.

Результаты:
- словарь сущностей;
- типы связей;
- визуальная семантика;
- M0–M3;
- трехслойная модель OTUS → Architect Pro → FATHER Production;
- AI Capability Map;
- Definition of Done.

Статус: **DONE / standard v1 created**.

## STEP 01 — Master Architecture Map

**Цель:** одна карта всей платформы, связывающая 31 урок и production capabilities.

Должны появиться:
- строгая схема с нотацией;
- отдельная яркая обзорная визуализация;
- capability-to-lesson matrix;
- capability-to-FATHER-component matrix;
- зоны ответственности и границы;
- GAP/UNKNOWN список.

## STEP 02 — Machine-readable Course Manifest

Вынести реестр уроков из `site/app.js` в данные.

Минимальная модель:
- id/title/gate;
- OTUS source and requirements;
- Architect Pro extensions;
- FATHER Production mapping;
- artifacts/evidence;
- maturity;
- links;
- visual assets.

## STEP 03 — Universal Lesson Template

Один шаблон страницы для всех уроков:

1. Hero.
2. Engineering schema.
3. Visual poster.
4. OTUS Curriculum.
5. Architect Pro.
6. FATHER Production.
7. Inputs/outputs.
8. Artifacts.
9. Tests/evidence.
10. Traceability.
11. Maturity.
12. Sources.

## STEP 04 — Lesson 01 normalization

Текущие `lesson-01.html` и `lesson-01-intake.html` переводятся на универсальный шаблон без потери уже сделанного Architect Intake Pack.

## STEP 05–35 — Lessons 02–31

Каждый следующий урок проходит общий pipeline. Номер STEP не равен номеру урока: STEP 05 соответствует Lesson 02, STEP 35 — Lesson 31.

Каждый урок обязан давать как минимум:
- схему;
- visual;
- OTUS layer;
- Architect Pro layer;
- FATHER Production layer;
- evidence/status.

## STEP 36 — Cross-Lesson Traceability

Матрица:

`BUS → REQ/NFR → RISK → ADR → CMP → CTRL → TEST → SLO → COST → REL`

Плюс AI capability relations:
`CTX/RAG/MEM/MODEL/MCP/GRAPH/AGENT/EVAL/SAFE/OBS/GATEWAY/FIN`.

## STEP 37 — Architecture Packs & Gates

Для G1–G7:
- отдельная страница;
- состав Architecture Pack;
- входные и выходные критерии;
- red flags;
- evidence completeness.

## STEP 38 — Automated Evidence

Статусы сайта перестают быть ручными там, где возможно:
- CI;
- tests;
- artifacts;
- PR/review;
- manifests;
- generated indexes.

## STEP 39 — Production Cockpit

Финальный слой:
- quality/SLO;
- agent/tool traces;
- RAG quality;
- security;
- cost;
- capacity;
- release/deployment;
- incidents;
- architecture debt.

## Обязательное правило

Перед началом следующего STEP предыдущий получает запись в `docs/DEVELOPMENT_JOURNAL.md`:
- что сделано;
- evidence;
- что стоит улучшить;
- как улучшить;
- приоритет;
- открытые GAP;
- следующий шаг.


## Out-of-order completion note — STEP 18

По запросу пользователя **STEP 18 / Lesson 15 Observability** выполнен приоритетно до STEP 16–17.

Это не меняет последовательную модель:

- STEP 16 = Lesson 13;
- STEP 17 = Lesson 14;
- STEP 18 = Lesson 15.

STEP 16–17 остаются pending. Завершённый STEP 18 не считается автоматическим закрытием предыдущих шагов.


## STEP 19 — Lesson 16 completed out of order

Lesson 16 / Sizing выполнен приоритетно по запросу пользователя.

Добавлен обязательный Agent Factory gate:

`SLO → SIZING → TCO → CAPACITY GATE → DEPLOY`

STEP 16–17 (Lessons 13–14) остаются pending.


## STEP 20 — Lesson 17 completed out of order

Lesson 17 / LLM Inference Sizing выполнен после Lesson 16 как единая capacity chain.

Agent production gates now include:

`SLO → CAPACITY GATE → INFERENCE GATE → COST → RELEASE`.

STEP 16–17 in the original sequential queue (Lessons 13–14) remain pending.
