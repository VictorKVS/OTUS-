# FATHER · Factory Manufacturing Model

Статус: **CANONICAL ARCHITECTURE v1**

## 1. Определение

FATHER — информационно-инженерная фабрика, которая принимает исходную информацию и последовательно перерабатывает её в проверенный проект / программное изделие / агентную систему.

**Агенты не являются фабрикой.** Агенты, модели, инструменты, базы знаний и runtime-компоненты являются рабочими единицами и оборудованием внутри производственных цехов.

## 2. Главный поток

```text
INPUT
  ↓
INTAKE / ПРИЁМКА
  ↓
ANALYSIS / АНАЛИТИЧЕСКИЙ ЦЕХ
  ↓
ARCHITECTURE / ПРОЕКТНЫЙ ЦЕХ
  ↓
KNOWLEDGE & DATA / ЦЕХ ЗНАНИЙ И ДАННЫХ
  ↓
AGENT & COMPONENT ENGINEERING / КОМПЛЕКТАЦИЯ
  ↓
IMPLEMENTATION / ПРОИЗВОДСТВО
  ↓
QA + SECURITY + LAB / ОТК И ИСПЫТАНИЯ
  ↓
DEVOPS / СБОРКА И СРЕДЫ
  ↓
ACCEPTANCE / ПРИЁМКА
  ↓
OUTPUT
```

## 3. Вход фабрики

Фабрика может принимать:
- идею;
- бизнес-задачу;
- ТЗ;
- документы;
- нормативные источники;
- данные;
- исходный код;
- существующую систему;
- требования заказчика;
- инцидент / проблему;
- запрос на модернизацию;
- проект предыдущей версии.

Вход никогда не идёт напрямую в разработку. Он проходит Intake и получает идентификатор, owner, scope, ограничения, источники и первичную классификацию.

## 4. Цех как универсальная производственная единица

Каждый цех обязан иметь один и тот же контракт:

```text
INPUT
↓
REGULATION / STANDARD
↓
RESPONSIBLE ROLE / AGENT
↓
PROCESS
↓
TOOLS / MODELS / KNOWLEDGE
↓
ARTIFACTS
↓
TESTS / VALIDATION
↓
EVIDENCE
↓
GATE
↓
OUTPUT
↓
NEXT WORKSHOP
```

Если нет обязательного артефакта, теста или evidence, Gate не может дать promotion.

## 5. Основные производственные цеха

### W00 Intake
Принимает сырьё, регистрирует проект, scope, владельца, ограничения и источники.

### W10 Analysis
ALINA и аналитические средства превращают разрозненную информацию в требования, факты, сущности, риски, ограничения, гипотезы и traceability.

### W20 Architecture
Архитектор превращает требования в HLD/LLD, contracts, ADR, C4/DFD/BPMN, NFR и Development Pack.

### W30 Knowledge & Data
Knowledge Engineer формирует K0/K1/K2 подключение, source registry, datasets, schemas, retrieval/data contracts.

### W40 Agent & Component Engineering
Подбираются Agent Kits, модели, инструменты, reusable blocks и project-specific components. Решение REUSE / ADAPT / NEW фиксируется.

### W50 Implementation
FATHER Programmer/CODEX реализует только утверждённый Development Pack и создаёт код, конфигурации и unit-level evidence.

### W60 QA / Security / LAB
Независимый контур проверяет функциональность, качество, безопасность, regression, performance и соответствие требованиям.

### W70 DevOps / Environments
Формирует build artifact, container, CI/CD, среды, telemetry, rollback и operational evidence.

### W80 Acceptance / Certification
Проверяет полный evidence bundle, acceptance criteria и разрешает или запрещает promotion.

### W90 Output / Delivery
Формирует готовый продукт и полный пакет его технического дела.

## 6. Выход фабрики

Выход — не только код.

```text
PRODUCT
+ SOURCE CODE
+ ARCHITECTURE
+ CONTROLLED DOCUMENTS
+ KNOWLEDGE PROFILE
+ TESTS
+ SECURITY RESULTS
+ LAB RESULTS
+ TRACE / EVIDENCE
+ BUILD / DEPLOYMENT
+ RUNBOOKS
+ CERTIFICATION STATUS
+ KNOWN LIMITATIONS
+ CHANGE / FEEDBACK LOOP
```

## 7. Регламенты и тесты

Регламент существует на трёх уровнях:

1. **Factory regulation** — общие правила FATHER.
2. **Workshop regulation** — правила конкретного цеха.
3. **Product profile / tailoring** — какие требования обязательны именно для данного класса изделия.

Тесты также многоуровневые:
- artifact validation;
- contract tests;
- unit/integration/system tests;
- security tests;
- LAB evaluations;
- environment checks;
- acceptance tests;
- production/regression checks.

## 8. Роль C00–C99

C00–C99 — индекс технического дела и контрольных областей изделия. Это не сама фабрика и не обязано быть 100 линейными операциями.

Цех Wxx может читать или производить несколько Cxx-артефактов. Например:

```text
W20 Architecture
  ├─ C04 HLD/C4
  ├─ C05 LLD/API
  ├─ C08 ADR
  └─ C09 Architecture Review
```

## 9. Роль агентов

```text
FACTORY
  ↓
WORKSHOP
  ↓
ROLE
  ↓
AGENT KIT / HUMAN
  ↓
TOOLS + KNOWLEDGE + MODELS
```

Один агент может работать в нескольких цехах только в рамках разрешённых ролей. Критические проверки должны оставаться независимыми от автора реализации.

## 10. Специализированные цеха

CyberED, Pentest, OSINT, Legal, Security, Visual, Mobile и другие направления не заменяют основной конвейер.

Они подключаются как специализированные производственные участки:

```text
MAIN FACTORY
   ├─ Security Workshop
   │    ├─ Security Engineer
   │    ├─ DevSecOps
   │    ├─ Pentest
   │    └─ Blue Team
   ├─ OSINT Workshop
   ├─ Knowledge Workshop
   └─ ...
```

## 11. Главная метрика фабрики

Не количество агентов и не количество документов.

Главная метрика:

> Может ли фабрика воспроизводимо превратить допустимый вход в проверенный выход, сохранив требования, traceability, evidence, безопасность и управляемость изменений.

## 12. Производственный закон

**NO REGULATION → NO PROCESS**

**NO TEST → NO CLAIM OF QUALITY**

**NO EVIDENCE → NO PROMOTION**

**NO ACCEPTANCE → NO RELEASE**