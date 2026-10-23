# FATHER Knowledge Architecture Standard

Статус: **CANONICAL DESIGN v1**

## 1. Главное правило

Каждый профессиональный агент FATHER наследует одну общую базу знаний и подключает одну или несколько специализированных баз.

~~~text
                    FATHER COMMON KNOWLEDGE CORE
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
      ALINA BASE          OSINT AGENT        FATHER CODEX
          │                   │                   │
          ▼                   ▼                   ▼
  Specialist Pack:      Specialist Pack:    Specialist Pack:
  Analytics             OSINT               Software Eng.
~~~

Формула:

`AGENT KNOWLEDGE = COMMON CORE + SPECIALIST PACK + optional PROJECT CONTEXT`

При этом Memory и Experience не являются Knowledge Base и хранятся отдельно.

## 2. K0 — FATHER Common Knowledge Core

Обязателен для всех агентов.

Содержит общие знания и правила, которые не должны заново преподаваться каждому специалисту:
- работа с источниками, документами и версиями;
- provenance, citations и evidence;
- факты, утверждения, сущности, связи, события и противоречия;
- базовые методы анализа и проверки;
- логика требований и traceability;
- стандарты FATHER: документы, gates, lifecycle, statuses;
- основы безопасной работы с данными и инструментами;
- общая терминология AI/LLM/RAG/agents/tools/workflows;
- общая цифровая и инженерная грамотность;
- правила письменной коммуникации и структурирования результата;
- правила uncertainty / confidence / abstention;
- общие anti-hallucination и source-grounding policies.

Common Core является централизованным, versioned и read-mostly для рабочих агентов. Изменения проходят FATHER LAB и regression, потому что изменение Common Core потенциально влияет на всех специалистов.

## 3. K1 — Specialist Knowledge Pack

Профессиональная база конкретного типа специалиста.

Примеры:
- `KB-OSINT` — OSINT;
- `KB-IB` — информационная безопасность;
- `KB-DEVSECOPS` — DevSecOps;
- `KB-LEGAL` — право;
- `KB-PROGRAMMER` — software engineering;
- `KB-ARCHITECT` — архитектура;
- `KB-PENTEST` — пентест;
- `KB-PROJECT` — project/product management.

Specialist Pack содержит:
- предметную терминологию;
- профильные первоисточники;
- нормативные/технические документы;
- методы и процедуры;
- типовые объекты и отношения графа;
- профессиональные кейсы;
- отраслевые ошибки и anti-patterns;
- профильные benchmarks/exams;
- links to skill tree.

## 4. K2 — Project / Organization Context (optional overlay)

Это не постоянная общая база и не профессиональная школа.

Слой содержит знания текущего проекта/организации:
- конкретные документы проекта;
- архитектуру продукта;
- локальные политики;
- внутренние API/схемы;
- бизнес-термины;
- текущие данные и артефакты.

K2 имеет более узкий scope и access policy. Он может быть удалён/сменён без изменения K0/K1.

## 5. Отдельно: Memory и Experience

Нельзя смешивать:

~~~text
KNOWLEDGE  = что специалист знает как проверяемое знание
SKILLS     = что специалист умеет делать
MEMORY     = что произошло в конкретной работе/диалоге/расследовании
EXPERIENCE = какой обобщённый урок получен из выполненных работ
~~~

Experience после проверки может породить Change Request в K0 или K1, но не записывается туда автоматически.

## 6. Knowledge inheritance

Каждый Agent Passport обязан ссылаться на:
- common_core_id;
- common_core_version;
- specialist_pack_ids + versions;
- optional project_context_id;
- retrieval policy;
- access policy;
- citation/provenance policy;
- freshness policy;
- conflict policy.

Никакого физического копирования Common Core в каждую базу специалиста. Агент наследует K0 логически через Knowledge Router.

## 7. Knowledge Router

~~~text
USER / TASK
    ↓
Intent + Domain Detection
    ↓
Knowledge Router
    ├── K0 Common Core
    ├── K1 Specialist Pack
    └── K2 Project Context
            ↓
Merge / Deduplicate / Rank / Conflict Check
            ↓
Evidence Bundle
            ↓
Agent / LLM
~~~

Router обязан сохранять provenance каждого фрагмента. Слияние результатов не должно стирать источник и версию.

## 8. Conflict policy

При конфликте источников агент не выбирает молча.

Алгоритм:
1. определить слой и источник каждого утверждения;
2. проверить version/date/authority;
3. показать contradiction;
4. применить domain policy;
5. при невозможности разрешения — сохранить обе версии и снизить confidence;
6. при необходимости отправить finding в ALINA Knowledge Lab.

Project Context не может без явной policy переписать нормативное/профессиональное знание K1.

## 9. Versioning and blast radius

Изменение K0 имеет большой blast radius и требует:
- impact analysis по всем dependent agents;
- regression по критическим specialist suites;
- staged rollout;
- rollback version.

Изменение K1 требует regression только зависимых специалистов/проектов.

K2 обновляется по правилам конкретного проекта.

## 10. ALINA School model

Обучение любого специалиста начинается с общей школы:

~~~text
K0 COMMON SCHOOL
→ common exam
→ K1 SPECIALIZATION
→ specialist exercises
→ tools/workflows
→ specialist exam
→ real practice
→ certification
~~~

То есть OSINT, IB, Programmer и другие специалисты получают одинаковый фундамент, но разную профессиональную специализацию.

## 11. Agent readiness gate

Агент не может получить статус CANDIDATE, если:
- Common Core не указан или несовместим;
- Specialist Pack отсутствует для профессиональной роли;
- source/provenance policy не определена;
- knowledge tests не пройдены;
- есть unresolved critical contradictions;
- knowledge versions не зафиксированы.

## 12. FATHER Specialist Mind

Итоговая модель:

~~~text
FATHER SPECIALIST MIND
│
├── K0 Common Knowledge Core
├── K1 Specialist Knowledge Pack
├── K2 Project Context (optional)
├── Skills
├── Memory
└── Experience
~~~

Это является стандартной когнитивной архитектурой всех профессиональных агентов FATHER.