# IDEA+ — SADEQ Enterprise Operations Copilot
**ID:** IDEA-2026-SADEQ-003 · **Редакция:** 0.3 · **Дата:** 2026-11-27 · **Статус:** PROPOSED / NOT APPROVED.

## 0. Решение об изменении базовой концепции
Предыдущая IDEA+ v0.2 сохраняется как исследовательский исходник. Новый объект проектирования — **один корпоративный агент технических заявок и регламентов** на универсальном UAA ядре. Фабрика множества агентов остаётся будущим развитием, а не условием первого релиза. Приоритеты изменены после [анализа вакансий, 27.11.2026](../MARKET_DRIVEN_MVP_2026_11/README.md). Изменение не означает фактического завершения предыдущих документов.

## 1. Идея и бизнес-проблема
Корпоративные операторы тратят время на поиск регламентов, анализ заявок, сопоставление событий и ручное перенесение предложений в Service Desk/ERP. Непрозрачные LLM-решения без разделения полномочий создают риск утечки данных, ошибочного действия и невозможности доказать результат. Нужен локальный помощник, который **обоснованно предлагает**, а действуют только разрешённые инструменты после политик и согласования.

## 2. Заинтересованные стороны и потребители
**Бизнес-пользователь:** инженер поддержки/оператор ITSM; **владелец данных:** контролирует источники и классификацию; **согласующий:** подтверждает точно сформированное изменение заявки; **администратор:** настраивает контур; **ИБ/SOC:** контролирует риски; **независимый экзаменатор:** POLYGON.
**Бенефициар проекта:** автор и инженерное портфолио для AI Engineer/AI Security/Enterprise Integration, а также OTUS AI Architect. Реальный коммерческий заказчик, бюджет и измеренный ROI не подтверждены.

## 3. Проверяемая ценность
Сократить ручное переключение между заявкой, документом и системой исполнения *как гипотеза*. Демонстрация обязана показать: входная заявка → цитаты из локальной БЗ → объяснимое предложение → проверка разрешений → согласование → запись в тестовую ITSM → независимая проверка состояния. Обещания экономии времени и качества запрещены до измерения baseline.

## 4. Утверждаемые цели и границы по фазам
### P0 — Карьерный MVP (первый сквозной работающий сценарий)
- Локальный inference без внешних AI API, FastAPI, PostgreSQL, Qdrant, контейнеризация и воспроизводимый запуск.
- Вход через API и загрузку документа; схема должна быть закрытой и версионированной.
- Импорт двух форматов (PDF и DOCX) из разрешённого синтетического набора, provenance/chunk IDs.
- RAG с видимыми цитатами на первоисточники, tenant ACL до выдачи содержимого, benchmark against lexical/vector baseline.
- Управляемый LangGraph-orchestrated workflow с checkpoint/retry/limits.
- UAG/Policy enforcement вне LLM; строго типизированный mock Service Desk tool; human approval для изменения заявки.
- Регистрация события, состояние, дедупликация, post-action verification.
- POLYGON как независимый исполняемый тестовый контур: функциональные, негативные, регрессионные, security-тесты, evidence.
- Наблюдаемость/метрики и демонстрационный веб-интерфейс.
### P1 — Итоговая OTUS-квалификация
- Реальный Neo4j GraphRAG с проверяемыми путями отношений и сравнением с vector-only.
- Три декларативных профиля на одном ядре для доказательства повторного использования (можно запускать на синтетических сценариях).
- K8s deployment, backup/restore, испытания offline/tenant-boundaries, measured sizing and TCO.
- Более строгий full SDLC и документационные комплекты, представление для комиссии.
### P2 — Research / future
- Agent 001 generates patch+tests in sandbox (не сам себя выпускает).
- Управляемое обновление знаний по feedback, прогнозирование при достаточной истории, более широкие коннекторы 1С/Bitrix24/n8n/MCP, обучение/адаптация моделей.
- Масштабирование фабрики/коммерческая продажа — только после пилота.

## 5. Что сознательно НЕ делаем в P0
Автономные высокорисковые операции, платежи, медицинский диагноз, эксплуатация реальных пациентских данных, облачные модельные API, обучение весов LLM, 20 агентов, обещание 10 000 LLM RPS, подтверждение сертификации или соответствия требованиям Минобороны, не имея договорных оснований.

## 6. Список желаемого → жёсткие ограничения
| ID | Driver | Тип | Решение |
|---|---|---|---|
| WD-01 | реальная корпоративная польза | желаемое | end-to-end заявка→решение→подтверждение |
| WD-02 | локальный, reproducible | обязательное P0 | deny egress, approved model artifacts |
| WD-03 | доказательный RAG | обязательное P0 | source/chunk/version citations |
| WD-04 | безопасные действия | обязательное P0 | allowlisted tool, separate policy, approval |
| WD-05 | воспроизводимость | обязательное P0 | events, checkpoints, ledger |
| WD-06 | качество | обязательное P0 | golden eval + negative suite |
| WD-07 | доказательство LLM/agent competencies | обязательное P0 | code, traces, results, demo |
| WD-08 | graph relationships | OTUS P1 | Neo4j graph path + measured comparison |
| HC-01 | запрет внешних LLM API | HARD | on-prem + egress-deny |
| HC-02 | запрет чтения чужих tenant данных | HARD | policy in retrieval/graph/cache/log |
| HC-03 | запрет agent self-approval и критических tool calls | HARD | independent deterministic controls |
| HC-04 | контракт-строгий поток | HARD | closed schemas, recipients, algorithm binding |
| HC-05 | никакой QUALIFIED без evidence | HARD | POLYGON, human release decision |
| HC-06 | реальный рабочий baseline должен укладываться в локальную лабораторию | HARD в лаборатории | Nvidia RTX3060 12GB / 32GB RAM; модель и throughput только после benchmark |

## 7. Пользовательские истории
| ID | История | Проверяемое завершение |
|---|---|---|
| US-01 | Инженер подаёт инцидент | trace+immutable event |
| US-02 | Инженер спрашивает регламент | цитата и ссылка на разрешённый фрагмент |
| US-03 | Агент предлагает исправление заявки | типизированный draft+source evidence |
| US-04 | Согласующий одобряет/отклоняет действие | точные параметры, время, actor, decision |
| US-05 | Владелец видит результат | подтверждённый authoritative ITSM state |
| US-06 | ИБ пытается выполнить запретный запрос | deny+audit без утечки |
| US-07 | Экзаменатор запускает оценку и регрессию | evidence с hash/version/expected/actual |
| US-08 | Архитектор объясняет tradeoff | ADR с альтернативами и измерениями |

## 8. Бизнес-схема

![SADEQ / FATHER — корпоративная бизнес-схема обработки заявки: 5 этапов, ALG-01…ALG-12, ветви отказа, RAG, UAG и проверка результата](diagrams/SADEQ_BUSINESS_FLOW_V03.svg)

> **Рисунок IDEA-BPM-01 — Основной бизнес-процесс SADEQ UAA (обзорная архитектурная инфографика, версия 0.3).**  
> [Открыть схему отдельно в полном размере](diagrams/SADEQ_BUSINESS_FLOW_V03.svg). Статус: **спроектировано / не квалифицировано**. Фирменная визуализация не является формальной BPMN 2.0 или схемой алгоритма по ГОСТ 19.701-90.

**Машинно-проверяемая последовательность (текстовая альтернативная версия):**  
`Authenticated ticket/document → ALG-01 validate → ALG-02 dedupe → ALG-03 object identity → ALG-04 event append → ALG-05 state → ALG-06 trigger → ALG-07 evidence retrieval → ALG-08 hypotheses → ALG-09 forecast if supported (else NOT_AVAILABLE) → ALG-10 policy-bound proposal → ALG-11 authorization/human → tool → ALG-12 authoritative verification → audit/review`.

**Ветки бизнес-решений:** `REJECT` — запрет при нарушении контракта; `REVIEW_REQUIRED` — неоднозначный объект; `NO_ACTION` — нет значимого события; `ABSTAIN` — недостаточно фактов; `NOT_AVAILABLE` — нет обоснованного прогноза; `APPROVAL_REQUIRED` — действие ждёт уполномоченного человека; `MISMATCH` — результат инструмента не подтверждён бизнес-системой. Все решения, за исключением оформления объяснения, проверяются детерминированными контролями.

### 8.1. Дополнительная визуализация для IDEA+ (план)
| ID | Иллюстрация | Что доказывает / поясняет | Приоритет |
|---|---|---|---|
| VIS-01 | Бизнес-процесс с ролями, BPMN/swimlanes | Кто действует: пользователь, UAA, UAG, согласующий, ITSM, POLYGON; где границы ответственности | P0 |
| VIS-02 | AS-IS → TO-BE, ценностная цепочка | Как меняется работа с обращением, без выдуманных процентов экономии | P0 |
| VIS-03 | C4 System Context + Container | Где система, интеграции, локальная LLM и хранилища; отсутствует внешний LLM API | P0 |
| VIS-04 | Схема доверия, угроз и UAG | User→Agent→Tool→Object, ACL, prompt injection, DENY, human gate | P0 |
| VIS-05 | RAG pipeline, provenance и graph paths | Документ→чанк→индекс→запрос→доказательство→ответ, различие P0/P1 | P0/P1 |
| VIS-06 | Диаграмма последовательности одного запроса | Обмен конкретными контрактами FLOW/API/ALG и обработка ошибок | P0 |
| VIS-07 | Матрица трассировки и quality gates | IDEA→FR→ALG→THR→TEST→EVI→POLYGON, что готово и что ещё нет | P0 |
| VIS-08 | Архитектура данных и состояний | Object/Event/Postgres/Qdrant/Neo4j/checkpoint; где Source of Truth | P1 |
| VIS-09 | Путь MVP P0→P1→P2 / OTUS | Границы первого работающего кейса, полного OTUS и исследовательского расширения | P0 |
| VIS-10 | Модель затрат, GPU sizing и рисков | Только измеренные данные и явно помеченные сценарии | После baseline |

**Стандарт визуального оформления:** единый SADEQ/FATHER navy/cyan/violet, читаемые названия, номер рисунка и версия, источники/трассировка, статус фактических доказательств, редактируемый SVG/Mermaid или BPMN-исходник, проверка ошибок и доступность подписи. Официальный документ по ГОСТ выпускается в отдельной проверенной форме, а не заменяется инфографикой.

## 9. Нефункциональные свойства и риски
**Security:** strict ACL, source provenance, prompt injection refusal, offline. **Reliability:** replay and idempotency. **Observability:** p95, TTFT, tokens/s, peak VRAM, trace/metrics; числа устанавливаем на baseline и измеряем. **Maintainability:** typed APIs, ADR, human commits, signed releases, SBOM and documented change control. **Data:** synthetic, rights-cleared, retention documented. **Risks:** cross-tenant leak, hallucination, wrong tool action, denial by local GPU, graph-index quality; threat matrix grows from IDEA+.

## 10. Успех и прекращение работы
P0 PASS только при работающем полном маршруте и сохранённых независимых evidence в целевой лаборатории. При незакрытом критичном тесте или несанкционированном tool call — NO-GO. При невозможности достижения качества RAG — пересмотреть retrieval, не «улучшать» отчёт. Product-market fit не заявляем до реальных интервью и пилотов.

## 11. Обоснование научно-инженерного выбора
- Gough/Bryant/Auburn *Mastering API Architecture*: C4, ADR, OpenAPI, contract tests.
- Suhas Pai *Designing Large Language Model Applications*: embedding/retrieval/reranking/GraphRAG.
- Antonio Gulli *Agentic Design Patterns*: routing, planning, tool use, checkpoints/memory.
- Chip Huyen *AI Engineering*: practical AI system evaluation, model choices and failure modes (точные главы проверять для каждого решения).
- Kubernetes Patterns: deployment research and benchmarking after P0.
Все решения оформляются как `SRC→ALG→PAT→ADR→TEST`, без выдачи книжной методики за подтверждённый результат.

## 12. Отличия новой редакции
Первый рабочий релиз перестал зависеть от 20 агентов, полной фабрики и прогнозов; реальный GraphRAG и три профиля перенесены в обязательный этап OTUS P1; независимость UAG и POLYGON сохранена; текущий карьерный результат — отдельный измеряемый сценарий Enterprise Operations Copilot.

**Следующий документ:** [ТЗ на АС по ГОСТ 34.602-2020](02_TECHNICAL_ASSIGNMENT_GOST_34_602.md).
