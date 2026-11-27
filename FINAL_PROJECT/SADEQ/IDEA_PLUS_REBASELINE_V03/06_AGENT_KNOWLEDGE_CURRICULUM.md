# SADEQ-CORPUS-001 — Учебные материалы и загрузка предметной базы знаний
**Версия:** 0.1 · **Статус:** CORPUS PLAN / NO TRAINING EXECUTED.

## 1. Подготовка материалов
| ID | Вид материалов | Состав набора | Алгоритм / роль | В P0 |
|---|---|---|---|---|
| MAT-01 | SLA и каталог услуг | приоритеты, классы инцидентов, правила эскалации | DMN ALG-06/10, role context | REQUIRED |
| MAT-02 | Стандартные инструкции и SOP | действия по типовым инцидентам, допустимые операции, версия, владелец | RAG ALG-07, цитаты | REQUIRED |
| MAT-03 | База известных ошибок / KB | сообщения, причины, проверенные решения, источники | case retrieval, ALG-07/08 | REQUIRED |
| MAT-04 | Синтетические заявки | ID, объект, симптомы, время, безопасные признаки | ALG-01..06, agent workflow | REQUIRED |
| MAT-05 | Справочник объектов | hostname/service key, owner, tenant, связи | ALG-03, B02 | REQUIRED |
| MAT-06 | API mock ITSM | versioned OpenAPI, examples, exact permissions | ALG-10..12, UAG | REQUIRED |
| MAT-07 | Политики доступа и действий | user→agent→tool→object, approval TTL | independent policy checks | REQUIRED |
| MAT-08 | Реестр схем и контрактов | JSON Schema with additionalProperties=false; recipient/algorithm binding | ALG-01 and FLOW | REQUIRED |
| MAT-09 | Набор эталонных случаев | ticket→expected evidence→expected action/refusal→actual state | evaluation / POLYGON | REQUIRED |
| MAT-10 | Attack fixtures | prompt injection, malicious documents, cross-tenant, stale approval | negative tests | REQUIRED |
| MAT-11 | История изменений и событий | synthetic events, late/duplicate/out-of-order | ALG-02/04/05/06 | REQUIRED |
| MAT-12 | Граф связей | verified assets/relationships/provenance | Neo4j GraphRAG | P1 |
| MAT-13 | Корпоративные инструкции эксплуатации | audit/runbooks/backup/incident | operators, SOC | P1 |
| MAT-14 | Прогнозные временные ряды | timestamped series + ground truth | ALG-09 baseline/backtest | P2, only if justified |

## 2. Обязательные метаданные каждого источника
`source_id, title, owner, classification, tenant_scope, allowed_purpose, version, effective_at, expires_at?, source_uri_or_file_ref, sha256, import_timestamp, parser_version, dataset_split, review_status`.
Для чанков дополнительно: `chunk_id, span/section/page, hash, embedding_model_version, acl_scope`. Графовые ребра могут быть сформированы только с привязкой к конкретному доказательству и независимой проверкой применимости.

## 3. Подготовка «обучающего» корпуса для агентов
1. Сформировать **синтетический** набор типовых задач, сообщений и первоисточников, достаточный для первых упражнений; точный объём фиксируем до baseline.
2. Разметить gold labels и желаемые конечные состояния; отрицательные кейсы включать заранее, а не по остаточному принципу.
3. Делить данные по кейсам и источникам, не только по строкам, на `DEV/TRAIN`, `VALIDATION`, `HELDOUT_TEST`. Не допускать копий и близких дубликатов между частями.
4. Отдельно выделить независимый **POLYGON hidden holdout** — агент и разработчик не редактируют оценочные критерии во время экзамена.
5. Избегать реальных ПДн, секретов, охраняемой технической документации и неразрешённых источников.

## 4. Способы обучения: принципиально разные операции
**A. Grounding / RAG:** загрузка, индексация, источники, ссылки; *не изменяет веса LLM*. Это наш P0.
**B. Tool/policy learning-by-specification:** агент получает спецификации разрешённых инструментов, алгоритмов и правил. Права и политика исполняются детерминированно вне модели.
**C. Prompt/workflow configuration:** отладка системных инструкций, LangGraph переходов, инструментальных шагов, memory/checkpoint. Проходит регрессию и версионирование.
**D. Supervised fine-tuning / LoRA:** изменение модели — **исследование P2**, только после проверки baseline/лицензии/quality delta/VRAM и отдельного security gate.
**E. Feedback:** предложения улучшения создаются из ошибок; публикация KB или prompt изменения после проверки и независимого теста, без self-training в проде.

## 5. Пакеты обучения (curriculum)
| Уровень | Задача агента | Педагогическая цель | Экзамен |
|---|---|---|---|
| L0 | использовать только схему и права | вход, отказ, происхождение | malformed / unknown sender → DENY |
| L1 | классифицировать заявку по каталогу | выделить тип и объект без фантазий | classification golden / abstain |
| L2 | найти точный регламент и пункт | evidence-first RAG | citation correct, no leak |
| L3 | сформировать конкурирующие гипотезы | поддержка/опровержение, неопределённость | contradiction case |
| L4 | предложить безопасное изменение заявки | typed action proposal | wrong tool/param not allowed |
| L5 | передать на согласование и проверить исход | hitl and policy | stale approval DENY, state verified |
| L6 | обработать конфликт/отказ/сбой | rollback/reconcile/retry bounds | interruption and duplicate suite |
| L7 | работать на новом профиле без копии ядра | specialization on shared UAA | P1 domain transfer |
| L8 | провести тестирование на отношениях | graph path validity | P1 GraphRAG benchmark |

## 6. Обязательные AI-алгоритмы и источники
- Hybrid/vector search, rerank, citations — Suhas Pai, *Designing Large Language Model Applications*, chapters 11–12.
- Routing, tool use, memory, bounded orchestration — Antonio Gulli, *Agentic Design Patterns*, relevant chapters.
- API-first, OpenAPI, contract tests — Gough/Bryant/Auburn, *Mastering API Architecture*.
- Production evaluation / failure design — Chip Huyen *AI Engineering*, exact edition chapter to be verified.
- Precise entity resolution, event sourcing and DMN require dedicated method cards and experiments; don't falsely attribute to these LLM books.

## 7. Evidence for corpus updates
`dataset_manifest.json, sha256 checksums, corpus build report, dedup report, labels review, legal/use rights approval, index build log, model/prompt hash, evaluation baseline` — all required to mark actual material READY.
