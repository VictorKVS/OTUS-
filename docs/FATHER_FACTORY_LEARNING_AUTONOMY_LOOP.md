# FATHER Factory Learning & Autonomy Loop

Статус: **CANONICAL DESIGN v1**

## 1. Главный принцип

FATHER не получает право автоматически производить систему только потому, что мы описали шаблон.

Право на автоматизацию зарабатывается последовательностью:

```text
MANUAL GOLDEN BUILD
→ REPEAT / HARDEN
→ EXTRACT INVARIANTS
→ COMPONENTIZE
→ CERTIFY BLOCKS
→ ASSISTED ASSEMBLY
→ AUTONOMOUS REPLICATION
→ COMPLEXITY INCREASE
→ NEW MANUAL GOLDEN BUILD
↺
```

## 2. Состояния зрелости

### M0 — METHOD DESIGN

Мы проектируем сам процесс FATHER:
- документы;
- C00–C99 dossier;
- stages/gates;
- evidence model;
- Agent Kit;
- Knowledge K0/K1/K2;
- LAB/DevOps/Trace.

Результат: есть метод, но ещё нет доказанного эталонного изделия.

### M1 — MANUAL GOLDEN REFERENCE

Первое изделие собирается **долго и вручную**.

На каждом этапе человек:
- открывает нужный Cxx;
- заполняет документ;
- принимает архитектурное решение;
- пишет/проверяет код;
- запускает тест;
- собирает trace/evidence;
- принимает PASS/FAIL/BLOCKED;
- фиксирует причины и исправления.

Автоматизация допускается только для механических действий, но не подменяет инженерные решения.

Цель M1 — не скорость. Цель — узнать, какой процесс действительно работает.

### M2 — REPEATED / HARDENED REFERENCE

Эталон повторяется на той же или очень близкой задаче.

Нужно доказать:
- шаги воспроизводимы;
- документы не являются случайными;
- gates ловят реальные ошибки;
- trace/evidence достаточны;
- повторная сборка не зависит от памяти конкретного человека;
- понятны обязательные и лишние шаги.

Только после повторения разрешено объявлять найденные части шаблоном.

### M3 — COMPONENTIZATION / SPARE PARTS

Стабильные элементы выделяются из проекта в reusable blocks.

```text
REFERENCE PRODUCT
   ↓
identify invariant
   ↓
extract block
   ↓
standard contract
   ↓
tests
   ↓
compatibility
   ↓
evidence
   ↓
BLOCK LIBRARY / ZOO
```

Примеры запасных частей:
- Telegram Channel Adapter;
- Trace Writer;
- TTS Provider Interface;
- STT Provider Interface;
- Knowledge Router;
- Agent Runtime;
- Retry/Error block;
- Evaluation Harness;
- Document generators;
- CI templates;
- observability hooks.

Проектная специфика не выносится в библиотеку без доказательства повторного использования.

### M4 — ASSISTED FACTORY

FATHER начинает собирать похожую систему из сертифицированных блоков, но человек ещё утверждает решения.

FATHER может автоматически:
- создать проект/Git/GitHub;
- развернуть C00–C99 dossier;
- подобрать chassis/profile;
- подобрать blocks REUSE/ADAPT/NEW;
- собрать документы из шаблонов;
- создать Agent Kits;
- подключить K0/K1/K2;
- сгенерировать конфигурацию;
- вызвать Programmer;
- построить tests/CI;
- прогнать validators/LAB;
- собрать evidence pack.

Но ключевые gates остаются human-approved.

### M5 — AUTONOMOUS REPLICATION

FATHER получает задачу того же класса и способен самостоятельно произвести аналогичное изделие end-to-end.

```text
BRIEF
→ classify product class
→ choose proven template/profile
→ assemble certified blocks
→ generate project dossier
→ implement project-specific delta
→ tests
→ LAB
→ security
→ environment
→ evidence
→ release candidate
```

Человек не ведёт каждый шаг вручную, а принимает итоговые критические gates и исключения.

Если FATHER встречает неизвестный блок или ситуацию вне доказанного класса — он обязан вернуть `NEW_BLOCK_REQUIRED / HUMAN_ENGINEERING_REQUIRED`, а не импровизировать production-решение.

### M6 — AUTONOMOUS PRODUCT FAMILY

FATHER умеет производить не один конкретный аналог, а семейство продуктов на общей платформе.

Он умеет выбирать:
- chassis;
- blocks;
- agent topology;
- models;
- channels;
- policies;
- environments;
- quality/cost profile.

Это уровень автомобильной платформы: одна технологическая база, разные комплектации.

### M7 — COMPLEXITY RATCHET

После успешной автоматизации мы намеренно повышаем сложность.

Но новый класс сложности **не наследует автоматически статус M5/M6**.

Для новой сложности создаётся новый learning loop:

```text
KNOWN AUTOMATED CLASS
        ↓
+ ONE MATERIAL COMPLEXITY DIMENSION
        ↓
NEW M1 GOLDEN REFERENCE
        ↓
M2 HARDEN
        ↓
M3 COMPONENTIZE
        ↓
M4 ASSIST
        ↓
M5 AUTONOMOUS REPLICATION
        ↓
NEXT COMPLEXITY
```

## 3. Правило одной новой сложности

По возможности на учебном витке добавляется одна крупная новая сложность за раз.

Пример лестницы:

```text
VOICE BRIDGE
text ↔ voice, one channel

→ MULTI-PROVIDER VOICE BRIDGE
provider routing / fallback

→ KNOWLEDGE AGENT
RAG + citations

→ OSINT SINGLE SPECIALIST
tools + evidence graph

→ OSINT MULTI-AGENT SYSTEM
collector + verifier + analyst + reporter

→ SECURITY / ISOLATED LAB
strict permissions + sandbox + adversarial tests

→ HIGH-LOAD / MULTI-TENANT
scale + tenant isolation
```

Каждый скачок сложности снова обязан пройти M1–M5.

## 4. Что значит «готово к библиотеке»

Компонент может стать стандартной запасной частью только если:
- использован минимум в эталонном проекте;
- имеет стабильный контракт;
- отделён от project-specific config;
- имеет unit/contract/integration tests;
- имеет failure modes;
- имеет security profile;
- имеет observability hooks;
- имеет compatibility/version;
- имеет evidence;
- имеет хотя бы один подтверждённый сценарий повторного использования или явно отмечен CANDIDATE до второго использования.

## 5. Что значит «FATHER умеет сам»

Недостаточно, что FATHER сгенерировал код.

Автономное производство считается доказанным только если FATHER сам:
1. правильно классифицировал задачу;
2. выбрал подходящий проверенный template/chassis;
3. собрал полный dossier;
4. выбрал reuse/adapt/new;
5. создал реализацию;
6. прошёл validators/tests;
7. прошёл LAB и security gates;
8. собрал evidence;
9. корректно остановился на неизвестности;
10. воспроизвёл результат на новой задаче того же класса.

## 6. Learning artifacts

Каждый ручной виток должен производить не только продукт, но и знания для фабрики:
- новый/исправленный template;
- reusable block;
- regression case;
- failure pattern;
- design rule;
- compatibility rule;
- evaluator;
- automation script;
- knowledge update;
- deprecated anti-pattern.

То есть продукт является одновременно **изделием и учебным стендом FATHER**.

## 7. Current pilot

`FATHER_VOICE_BRIDGE` является первым кандидатом на `M1 MANUAL GOLDEN REFERENCE`.

Его задача специально примитивна: проверить весь путь фабрики при минимуме предметной сложности.

Пока не существует реального end-to-end evidence и повторной сборки, он не переводится в M2/M3 и его блоки не считаются CERTIFIED.