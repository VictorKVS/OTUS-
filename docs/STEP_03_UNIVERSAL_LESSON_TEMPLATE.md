# STEP 03 — Universal Lesson Template

Статус: **IN PROGRESS**

## 1. Цель

Создать единый шаблон страницы, который будет использоваться для всех 31 уроков и не даст смешивать учебную программу, профессиональное расширение и production implementation.

## 2. Обязательная структура страницы

`SCHEMA → VISUAL → OTUS → ARCHITECT PRO → FATHER PRODUCTION → ARTIFACTS → TESTS/EVIDENCE → TRACEABILITY → MATURITY → SOURCES`

## 3. Нотационная схема

```mermaid
flowchart TB
    META[Lesson Manifest] --> HERO[Hero / Purpose]
    HERO --> SCH[Engineering Schema]
    SCH --> VIS[Visual Poster]
    VIS --> OTUS[OTUS Curriculum]
    OTUS --> PRO[Architect Pro]
    PRO --> FTH[FATHER Production]
    FTH --> ART[Artifacts]
    ART --> EV[Tests / Evidence]
    EV --> TR[Traceability]
    TR --> MAT[Maturity M0–M3]
    MAT --> SRC[Sources / Provenance]
```

## 4. Data contract

Шаблон получает из `course-manifest.json`:

- id/title/gate/status/maturity;
- source path;
- Architect Pro page/state;
- capability IDs.

Дополнительные lesson-specific данные должны храниться отдельно от layout.

## 5. Visual contract

Каждая lesson page имеет:

1. инженерную схему;
2. отдельный визуальный poster/infographic;
3. одну и ту же легенду цветов/форм из STEP 00;
4. подпись STEP / LESSON / maturity;
5. accessible text alternative.

## 6. UX layout

- sticky top navigation;
- Hero;
- схема;
- visual;
- 3-layer switch/sections;
- artifact/evidence cards;
- traceability strip;
- maturity panel;
- sources.

## 7. Definition of Done

- создан reusable template;
- создан visual poster template;
- данные отделены от layout;
- Lesson 01 мигрирован без потери Intake Pack;
- responsive layout;
- dark/light theme;
- ссылки на Git evidence;
- запись в journal.

## 8. Первый потребитель

**Lesson 01** используется как эталон миграции в STEP 04.
