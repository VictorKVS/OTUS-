# P1 — INTERNAL SCOUT · Сверка повторно используемых компонентов
**Проект:** SADEQ UAA · **Версия:** v0.2 · **Дата:** 27.11.2026  
**Статус:** STATIC_CODE_REVIEW_COMPLETED / TEST_EXECUTION_NOT_PERFORMED / REUSE_NOT_QUALIFIED.

## Область и метод
Проведён выборочный просмотр доступных исходных файлов, тестов и структуры нескольких действующих прототипов. Смотрели конкретные реализации, а не только README. Доказательство наличия кода и наличия тестового файла — **не** доказательство прохождения тестов, безопасности и совместимости. Исходные обозначения и адреса закрытых инженерных активов не публикуются в презентационном каталоге; полная трассировка хранится отдельно у владельца.

Проверены шесть функциональных групп: (1) workflow engine, (2) ingestion/text, (3) evidence/provenance, (4) event intake/audit, (5) learning curricula, (6) engineering/qualification designs. Прямой проверки локального исполнения на железе, licence inventory, SBOM, dependencies scan, runtime benchmarks и кросс-компонентной интеграции не было.

## REUSE_MATRIX (данные осмотра)
| ID | Узел | Наблюдаемый код/тесты | Статус | Решение | Причина и работа |
|---|---|---|---|---|---|
| SDC-001 | Work-process registry, шаги и состояния | Python + SQLite, регистрация процессов, состояние RUN/STEP, тестовый файл с in-memory SQLite | CODE_PRESENT / TEST_SOURCE_PRESENT | ADAPT | Существующий движок строго последовательный; не заменяет LangGraph/state-machine с ветвлениями, checkpoint и approval; нужны API adapter, tenant model |
| SDC-002 | Модуль извлечения текста документов | Python extraction PDF/office/ebook, bounded processing, fallback OCR в отдельных файлах | CODE_PRESENT | ADAPT | Проверить форматы, OCR зависимость, provenance на уровне страницы, безопасность обработки недоверенных файлов |
| SDC-003 | Evidence quality scorer | Python dataclasses, категории надёжности/relevance/independence/recency/directness/corroboration/provenance | CODE_PRESENT | ADAPT | Полезно как объяснимая эвристика; не является истинностью или независимым экспертом; требуется validation/benchmarks |
| SDC-004 | Knowledge record / append audit store | Python JSONL, stable IDs, append audit, unit tests исходники | CODE_PRESENT / TEST_SOURCE_PRESENT | ADAPT | Переход на PostgreSQL, транзакции, multi-tenant ACL, corruption/recovery tests |
| SDC-005 | Offline event intake | Python SQLite, URL normalization, fingerprint deduplication, timezone checks, audit log + unit tests | CODE_PRESENT / TEST_SOURCE_PRESENT | ADAPT | Поддерживает идеи безопасного intake; схема пока предметная; нужны generic Observation/Event и cross-channel entity resolution |
| SDC-006 | Learning object / curriculum | Структура учебных объектов, каталог, источники, шаблоны | DOCUMENTED | RESEARCH | Нельзя считать готовой системой обучения/подкрепления; требуются validator, evaluation harness и feedback gate |
| SDC-007 | Engineering agent / factory | README и документы описывают инженерную линию; структурированного runtime в просмотренных каталогах не найдено | DESIGN_ONLY_IN_INSPECTED_SCOPE | BUILD/RESEARCH | Нельзя заявлять готового автономного программиста; создать минимальный bootstrap agent с внешним approval |
| SDC-008 | Independent qualification lab | Документы/дорожные карты, не подтверждённый исполняемый набор испытаний | DESIGN_ONLY_IN_INSPECTED_SCOPE | BUILD | Отдельный независимый runner, holdout fixtures, signed evidence |
| SDC-009 | Production LangGraph + GraphRAG + UAG | В проверенном наборе исходников не подтверждена совместимая полная интеграция | NOT_VERIFIED | INTEGRATE/BUILD | Отдельная архитектура и PoC обязательны |

### Пример исполняемых инвариантов для переноса
- Ведущий журнал входных событий должен сохранять оригинальную запись и отметки времени; повторный импорт не должен дважды инициировать действие.
- Проверка доступности шага и контролируемого перехода состояния должна быть независима от генерации текста LLM.
- Верификация источника зависит от идентифицируемого доказательства, не от уверенности модели.
- Сбор учебных примеров и корректировки правил должен иметь versioning и независимую регрессию.

## Контрольные входы для адаптации (Design → Contract → Qualification)
| Компонент | Тест-интерфейс SADEQ | Доказательство, необходимое для `REUSE` |
|---|---|---|
| SDC-001 | `WorkflowStateStore` | branch/checkpoint/replay, concurrency, tenant isolation, approval negative tests |
| SDC-002 | `DocumentExtractor` | file sandbox, source page references, PDF and OCR accuracy tests |
| SDC-003 | `EvidenceEvaluator` | calibrated scoring against independent expert-labeled set |
| SDC-004 | `EventAuditRepository` | durability, idempotency, migration and restore tests |
| SDC-005 | `ChannelAdapter` | cross-channel identity, malformed payload, poison input, observability |
| SDC-006 | `CurriculumProvider` | test/feedback provenance, controlled promotion/rollback |
| SDC-007 | `EngineeringAgent` | source-to-patch + external independent test and human approval |
| SDC-008 | `QualificationRunner` | test isolation, tamper resistance, reproducible evidence |
| SDC-009 | `UAA Runtime` | offline end-to-end LangGraph+GraphRAG+ACL+policy qualification |

## Findings, blockers, gates
1. **Найден реальный код** для обработки процессов, извлечения, оценки доказательств, хранения и event intake; в отдельных узлах есть исходные unit-тесты.
2. **Не подтверждена единая работающая платформа.** Не показано общее исполнение ни одного полного цикла `multi-channel→object→event→GraphRAG→policy→action→feedback`.
3. **Нельзя объявить код REUSE-ready:** нет проведённых тестов, commit pinning в рабочем сборочном пакете, оценки лицензий и интеграционных контрактов. До квалификации использовать решение ADAPT/RESEARCH.
4. Нужен **offline license and supply chain gate** для исходных моделей, графовых DB, индексов, OCR, импортированных библиотек и датасетов. Готовность к коммерческому развёртыванию UNKNOWN.
5. Без независимой security-аттестации агент остаётся T0/T1; любые внешние/необратимые действия по умолчанию запрещены.

## P1 Verdict
**PARTIAL PASS — документирован code-aware reuse audit на выборочной группе компонентов.**  
Разрешён **контролируемый read-only PoC** с адаптацией SDC-001–005.  
**Не разрешено:** производство, статус VERIFIED/QUALIFIED, самостоятельное повышение прав, заявленные показатели производительности или экономика.

## P1 → P2 handoff
- Зафиксировать SHA коммитов и прямые пути в закрытом evidence-register.
- Собрать с lockfile в изолированном окружении и реально выполнить unit tests.
- Получить licence manifests, SBOM, reports для каждой переиспользуемой зависимости.
- Подготовить P2 world scout по 6 предметам: state machine; entity resolution/event sourcing; GraphRAG; scoped trust/policy; education evaluation; local model serving.
- Проверить первый falsifiable scenario: два канала → один объект → два события → replay state → deny external action.

**Принцип:** ни название проекта, ни README, ни наличие тестового файла не доказывают READY.
