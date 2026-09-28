# AI Capability Stack 2026 — Deep Dive

Основа списка — присланная пользователем схема «2023 → 2026». Здесь термины разложены не как мем/чеклист, а как инженерные capability.

## Важное уточнение

В исходной картинке рядом стоят разные по природе вещи: открытые протоколы, архитектурные паттерны, инженерные дисциплины, инфраструктура и методы обучения моделей. Поэтому в нашем сайте для каждой позиции фиксируется `kind`, уровень, входы/выходы, риски и FATHER mapping.

`RAG 2.0`, `Harness`, `Loop Engineering`, `Graph Engineering`, `Stateless MCP` — не единые формальные стандарты. В резюме и на собеседовании их нужно раскрывать конкретными механизмами, а не использовать как buzzwords.

## AI Harness

**Тип:** Platform runtime pattern  
**Целевой уровень:** L2–L3

Общий runtime-контур, который оборачивает вызовы моделей, tools, retrieval, policies, tracing и retries в единый управляемый слой.

**Зачем:** Не давать каждому AI-сервису самостоятельно реализовывать одинаковые integration/security/observability механизмы.

**Pipeline:** `App → Harness → Context/RAG → Model/Agent → Tool → Validation/Trace`

**Входы:** request, identity/claims, context, policy, model/tool config.

**Выходы:** validated response, tool results, trace, metrics, audit events.

**Типовые риски:** монолитный mega-wrapper; скрытая магия без прозрачных контрактов; single point of failure.

**Mapping:** `FTH-HARNESS-001`, `FTH-GTW-001`, `FTH-OBS-001`.

**Вопрос собеседования:** Что должен делать AI Harness, а что нужно оставить бизнес-сервису?

## Context Engineering

**Тип:** Engineering discipline  
**Целевой уровень:** L3

Проектирование полного контекста модели: instructions, retrieved knowledge, memory, tool results, user state и ограничения.

**Зачем:** Повысить качество и управляемость ответа без попытки решить всё одним prompt.

**Pipeline:** `Intent → Context selection → Retrieval/Memory → Compression/Ordering → Prompt assembly → Model`

**Входы:** user intent, system policy, retrieved chunks, memory, tool outputs.

**Выходы:** bounded context package, provenance metadata.

**Типовые риски:** context overflow; conflicting instructions; stale memory; data leakage.

**Mapping:** `FTH-CTX-001`, `FTH-PRM-001`, `FTH-KNW-001`, `FTH-MEM-001`.

**Вопрос собеседования:** Чем context engineering отличается от prompt engineering?

## Loop Engineering

**Тип:** Agent/workflow practice  
**Целевой уровень:** L2

Проектирование повторяющегося цикла perceive/decide/act/observe с явными условиями остановки, retries и budget limits.

**Зачем:** Сделать агентный цикл предсказуемым и не допустить бесконечных или дорогостоящих проходов.

**Pipeline:** `Observe → Decide → Act → Validate → Update state → Stop/Repeat`

**Входы:** goal, state, tool results, budgets.

**Выходы:** next action, updated state, final result.

**Типовые риски:** infinite loops; tool thrashing; cost explosion; state drift.

**Mapping:** `FTH-WFG-001`, `FTH-AGT-001`, `FTH-FIN-001`.

**Вопрос собеседования:** Какие stop conditions и budgets должны быть у agent loop?

## Graph Engineering

**Тип:** Workflow/state-machine practice  
**Целевой уровень:** L2–L3

Представление AI-workflow как графа узлов, переходов, условий, состояния и error paths.

**Зачем:** Делать сложный workflow наблюдаемым, тестируемым и управляемым вместо неявной цепочки prompts.

**Pipeline:** `State → Node → Conditional edge → Node/Tool → State update → End`

**Входы:** workflow state, events, policies.

**Выходы:** state transitions, execution trace.

**Типовые риски:** слишком сложный граф; неявные side effects; трудная отладка циклов.

**Mapping:** `FTH-WFG-001`, `FTH-SUP-001`, `FTH-OBS-001`.

**Вопрос собеседования:** Когда graph/state-machine лучше свободного agent loop?

## MCP

**Тип:** Open protocol / integration standard  
**Целевой уровень:** L1–L2

Протокол унифицированного подключения AI-приложений к tools/resources/prompts через MCP client/server.

**Зачем:** Снизить количество bespoke-интеграций между агентами и внешними системами.

**Pipeline:** `Host → MCP Client → MCP Server → Tool / Resource / Prompt`

**Входы:** capabilities, tool/resource requests, auth context.

**Выходы:** tool/resource results, protocol events.

**Типовые риски:** ошибка считать MCP security boundary; избыточные permissions; непроверенные servers/tools.

**Mapping:** `FTH-MCP-001`, `FTH-TOL-001`, `FTH-POL-001`.

**Вопрос собеседования:** Что MCP стандартизирует, а что он не решает автоматически?

## Stateless MCP

**Тип:** Deployment pattern, not separate standard  
**Целевой уровень:** L1–L2

Архитектурный вариант MCP-сервиса, где критичное состояние не хранится в локальной session memory сервера между запросами.

**Зачем:** Упростить горизонтальное масштабирование, recovery и cloud/serverless deployment.

**Pipeline:** `Request + identity + explicit state → MCP server → Tool → Response`

**Входы:** self-contained request, external/shared state reference.

**Выходы:** response without hidden local session dependency.

**Типовые риски:** потеря полезного session context; перенос state complexity во внешнее хранилище; ошибки idempotency.

**Mapping:** `FTH-MCP-001`, `FTH-REL-001`.

**Вопрос собеседования:** Почему stateless MCP удобнее масштабировать и где всё равно живёт state?

## Agentic AI

**Тип:** Architecture pattern  
**Целевой уровень:** L2–L3

AI-система, где модель участвует в выборе действий и может использовать tools в цикле до достижения цели.

**Зачем:** Решать задачи, где заранее нельзя полностью прописать последовательность шагов.

**Pipeline:** `Goal → Observe → Decide → Tool/Action → Result → Replan/Finish`

**Входы:** goal, state, tools, policies.

**Выходы:** actions, artifacts, final answer.

**Типовые риски:** excessive agency; unsafe tool use; nondeterminism; unbounded cost.

**Mapping:** `FTH-AGT-001`, `FTH-TOL-001`, `FTH-POL-001`.

**Вопрос собеседования:** Чем agent отличается от deterministic workflow?

## Multi-Agent Systems

**Тип:** Architecture pattern  
**Целевой уровень:** L2

Несколько агентов с разделёнными ролями, контекстами, tools или зонами ответственности.

**Зачем:** Разделять сложные задачи и ограничения, когда один агент становится слишком перегруженным.

**Pipeline:** `Supervisor/Router → Specialist agents → Review/Aggregation → Result`

**Входы:** task decomposition, agent roles, shared or isolated state.

**Выходы:** specialist results, handoffs, aggregated result.

**Типовые риски:** coordination overhead; контекстные конфликты; дорогие лишние вызовы; сложная трассировка.

**Mapping:** `FTH-AGT-001`, `FTH-SUP-001`, `FTH-WFG-001`.

**Вопрос собеседования:** Когда multi-agent хуже одного агента или обычного workflow?

## RAG 2.0

**Тип:** Umbrella term, not formal standard  
**Целевой уровень:** L2–L3

Условное название production-RAG: hybrid retrieval, reranking, query rewriting/routing, metadata/ACL, GraphRAG, eval и provenance.

**Зачем:** Уйти от простого 'embedding → top-k → prompt' к управляемой retrieval-системе.

**Pipeline:** `Query → Rewrite/Route → Dense+Sparse/Graph → Fusion → Rerank → ACL/Context → LLM → Citation/Eval`

**Входы:** query, identity, indexes, metadata, graph.

**Выходы:** ranked authorized context, grounded answer, citations.

**Типовые риски:** маркетинговая неопределённость термина; сложность без измеримого выигрыша; retrieval leakage.

**Mapping:** `FTH-KNW-001`, `FTH-RAG-001`, `FTH-EVL-001`.

**Вопрос собеседования:** Что вы называете RAG 2.0 и какие улучшения должны подтверждаться метриками?

## Memory Layers

**Тип:** Architecture pattern  
**Целевой уровень:** L2

Разделение памяти на short-term context, working state, episodic/history, semantic/knowledge и long-term profile.

**Зачем:** Не смешивать текущую задачу, историю пользователя и постоянные знания в одном бесконтрольном prompt.

**Pipeline:** `Event → Memory policy → Short/Working/Long-term store → Retrieval → Context`

**Входы:** conversation events, workflow state, facts, retention policy.

**Выходы:** selected memory context, updated durable memory.

**Типовые риски:** privacy; stale/false memories; неограниченный retention; cross-user leakage.

**Mapping:** `FTH-MEM-001`, `FTH-CTX-001`, `FTH-POL-001`.

**Вопрос собеседования:** Какие типы memory вы бы разделили и кто решает, что записывать навсегда?

## Tool Use

**Тип:** Agent capability  
**Целевой уровень:** L2–L3

Возможность модели/агента выбирать разрешённый внешний инструмент для получения данных или выполнения действия.

**Зачем:** Расширить систему за пределы генерации текста.

**Pipeline:** `Model proposes tool → Policy/Validation → Execute → Result → Model`

**Входы:** tool registry, schemas, permissions, model decision.

**Выходы:** tool call, validated tool result.

**Типовые риски:** over-permission; prompt injection to tool; side effects; bad arguments.

**Mapping:** `FTH-TOL-001`, `FTH-POL-001`, `FTH-OBS-001`.

**Вопрос собеседования:** Почему tool execution нельзя доверять одной только LLM?

## Function Calling

**Тип:** Model/API capability  
**Целевой уровень:** L2

Структурированный способ, при котором модель формирует имя функции/tool и аргументы по заданной schema.

**Зачем:** Связать natural language decision с программным интерфейсом без парсинга свободного текста.

**Pipeline:** `Tool schema → Model → {name,args} → Validation → Function → Result`

**Входы:** tool schema, user/context.

**Выходы:** structured tool invocation.

**Типовые риски:** schema-valid ≠ business-valid; hallucinated/unsafe args; неверный tool selection.

**Mapping:** `FTH-TOL-001`, `FTH-HARNESS-001`.

**Вопрос собеседования:** Чем function calling отличается от фактического выполнения функции?

## Vector Databases

**Тип:** Data infrastructure  
**Целевой уровень:** L2

Хранилища/индексы для embeddings и similarity search; могут быть специализированными или расширением обычной БД.

**Зачем:** Быстро находить семантически близкие chunks/items.

**Pipeline:** `Text → Embedding → Vector index; Query → Embedding → ANN search → candidates`

**Входы:** vectors, metadata, filters.

**Выходы:** nearest candidates, scores.

**Типовые риски:** игнорирование lexical search; неправильная distance metric; ACL/metadata filtering after retrieval.

**Mapping:** `FTH-RAG-001`, `FTH-KNW-001`.

**Вопрос собеседования:** Когда pgvector достаточно, а когда нужен отдельный vector database?

## Fine-tuning

**Тип:** Model adaptation technique  
**Целевой уровень:** L1–L2

Дополнительное обучение базовой модели на специализированных данных для изменения поведения/стиля/способности решать определённый класс задач.

**Зачем:** Когда prompt/RAG недостаточно для устойчивого поведения или specialized task.

**Pipeline:** `Curated dataset → Train/adapt → Evaluate → Register → Deploy`

**Входы:** training examples, base model, evaluation set.

**Выходы:** adapted model/checkpoint.

**Типовые риски:** data quality; overfitting; forgetting; training cost; license/privacy.

**Mapping:** `FTH-MDL-001`, `FTH-MRG-001`, `FTH-EVL-001`.

**Вопрос собеседования:** Когда fine-tuning оправдан, а когда лучше RAG?

## Evaluation Frameworks

**Тип:** Quality engineering  
**Целевой уровень:** L2–L3

Система тестовых datasets, evaluators, experiments и regression gates для измерения AI-качества.

**Зачем:** Заменить 'кажется, стало лучше' воспроизводимым сравнением.

**Pipeline:** `Golden set → Run → Deterministic/LLM/Human eval → Metrics → Compare → Gate`

**Входы:** test cases, expected outputs/sources, traces.

**Выходы:** metrics, failures, regression decision.

**Типовые риски:** метрики не отражают бизнес-ценность; judge bias; test leakage; малый dataset.

**Mapping:** `FTH-EVL-001`, `FTH-OBS-001`.

**Вопрос собеседования:** Какие проверки AI-системы можно сделать детерминированно, а где нужен human/LLM judge?

## Guardrails

**Тип:** Safety/security control layer  
**Целевой уровень:** L2

Совокупность ограничений вокруг input, retrieval, model output и tool actions.

**Зачем:** Не считать prompt единственной линией защиты.

**Pipeline:** `Input policy → Retrieval ACL → Model → Output/schema policy → Tool policy → Audit`

**Входы:** policy, identity, content, tool calls.

**Выходы:** allow/deny/transform/escalate decisions.

**Типовые риски:** ложное чувство безопасности; обходы; слишком жёсткие false positives.

**Mapping:** `FTH-POL-001`, `FTH-HARNESS-001`.

**Вопрос собеседования:** Что такое guardrails без маркетинга и почему это не одна библиотека?

## Observability

**Тип:** Operations discipline  
**Целевой уровень:** L2–L3

Трассировка и измерение prompts, retrieval, tool calls, model usage, latency, cost, errors и outcomes.

**Зачем:** Понимать, почему AI-система дала конкретный результат и где возник сбой.

**Pipeline:** `Request → Spans/Traces/Metrics/Logs → Correlation → Dashboard/Alert → Investigation`

**Входы:** runtime events, trace IDs, model/tool metadata.

**Выходы:** traces, metrics, alerts, audit evidence.

**Типовые риски:** логирование чувствительных данных; дорогая телеметрия; нет корреляции end-to-end.

**Mapping:** `FTH-OBS-001`, `FTH-EVL-001`, `FTH-FIN-001`.

**Вопрос собеседования:** Что логировать в RAG/agent trace и что нельзя писать в лог бездумно?

## Prompt Optimization

**Тип:** Optimization practice  
**Целевой уровень:** L2

Систематическое улучшение prompt/templates по eval-набору, а не ручная правка на отдельных примерах.

**Зачем:** Повышать task success/format adherence/robustness с контролем регрессий.

**Pipeline:** `Prompt version → Eval run → Error analysis → Candidate change → A/B/Regression → Promote`

**Входы:** prompt versions, eval set, metrics.

**Выходы:** versioned prompt, comparison report.

**Типовые риски:** overfit to eval set; prompt bloat; скрытая зависимость от одной модели.

**Mapping:** `FTH-PRM-001`, `FTH-EVL-001`.

**Вопрос собеседования:** Как вы докажете, что новый prompt лучше старого?

## Synthetic Data

**Тип:** Data engineering technique  
**Целевой уровень:** L1–L2

Искусственно сгенерированные примеры для training/eval/stress/security scenarios, прошедшие quality checks.

**Зачем:** Расширять редкие сценарии и тестировать систему без раскрытия части реальных данных.

**Pipeline:** `Scenario/spec → Generate → Filter/Validate → Deduplicate → Human sample review → Dataset`

**Входы:** scenario taxonomy, generation model/rules, quality criteria.

**Выходы:** synthetic examples, labels, provenance.

**Типовые риски:** model bias copied into dataset; duplicates; synthetic artifacts; false confidence.

**Mapping:** `FTH-SYN-001`, `FTH-EVL-001`.

**Вопрос собеседования:** Как убедиться, что synthetic dataset не ухудшает evaluation?

## Distillation

**Тип:** Model compression/adaptation technique  
**Целевой уровень:** L1

Обучение меньшей student-модели воспроизводить поведение/распределения более сильной teacher-модели.

**Зачем:** Снизить latency/cost и получить компактную специализированную модель.

**Pipeline:** `Teacher outputs/logits → Training data → Student → Evaluation → Deploy`

**Входы:** teacher, student, task data, eval set.

**Выходы:** smaller adapted model.

**Типовые риски:** потеря качества; наследование ошибок teacher; дорогая подготовка данных.

**Mapping:** `FTH-MDL-001`, `FTH-EVL-001`, `FTH-FIN-001`.

**Вопрос собеседования:** Чем distillation отличается от обычного fine-tuning?

## AI Gateways

**Тип:** Platform infrastructure pattern  
**Целевой уровень:** L2–L3

Единая точка доступа к нескольким model providers/backends с routing, quotas, auth, fallback, logging и cost control.

**Зачем:** Не связывать бизнес-код напрямую с конкретным LLM provider.

**Pipeline:** `App → AI Gateway → Policy/Route → Model A/B/Local → Response/Trace`

**Входы:** request, identity, routing policy, provider configs.

**Выходы:** provider response, usage/cost telemetry, fallback result.

**Типовые риски:** gateway bottleneck; provider-specific features leak; centralized secret exposure.

**Mapping:** `FTH-GTW-001`, `FTH-FIN-001`, `FTH-OBS-001`.

**Вопрос собеседования:** Что должен делать AI Gateway и почему это не просто reverse proxy?

## Cost Optimization / AI FinOps

**Тип:** Economics/operations discipline  
**Целевой уровень:** L2

Управление затратами на tokens, model choice, caching, retrieval, batching, GPU capacity и agent steps при сохранении SLO/quality.

**Зачем:** Оптимизировать unit economics AI-системы, а не просто выбирать самую дешёвую модель.

**Pipeline:** `Measure usage → Attribute cost → Compare quality/SLO → Optimize → Budget/Alert → Re-evaluate`

**Входы:** tokens, latency, GPU/API usage, quality metrics, business volume.

**Выходы:** unit cost, budgets, routing rules, savings experiments.

**Типовые риски:** экономия ценой качества; неучтённый retrieval/tool cost; agent loop explosion.

**Mapping:** `FTH-FIN-001`, `FTH-GTW-001`, `FTH-EVL-001`.

**Вопрос собеседования:** Какие оптимизации стоимости вы примените до перехода на более дешёвую модель?

## Как использовать

Для каждого capability на сайте применяем шаблон:

`Definition → Why → Flow → Inputs/Outputs → Risks → FATHER Mapping → Interview Question → Evidence`

READY ставится только когда capability можно объяснить за 60–90 секунд, нарисовать и связать с реальным WORK/PROJECT/LAB evidence.