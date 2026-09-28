# LLM & RAG Interview Playbook

## LLM integration — ответ за 60 секунд

LLM в приложении — управляемый компонент, а не чат. Приложение формирует instructions/context, вызывает модель, валидирует ответ и только после этого передаёт результат дальше.

Схема: `Application → Prompt/Context → Model Gateway → API/Local Inference → Validation → Result`.

При выборе модели сравниваю качество на собственном eval set, context window, latency, стоимость, structured output/tool calling, требования к данным, возможность local/on-prem и сложность эксплуатации.

## Prompt engineering

Prompt рассматриваю как программный контракт: system instructions, task, context, examples, constraints, output schema. Сильная формулировка: «определяю входы, ограничения, контракт результата и критерии ошибки».

## Structured output

Результат модели должен проходить `parse → schema validation → deterministic checks → retry/fallback → audit`. Для интеграций предпочтителен JSON/JSON Schema/Pydantic-подобный контроль.

## RAG pipeline

`Sources → Ingestion → Parsing → Cleaning → Chunking → Metadata → Embeddings/Indexes → Retrieval → Reranking → Context Assembly → LLM → Answer + Sources`

**Ingestion:** стабильный document ID, source, version, timestamps, metadata и сохранение происхождения.

**Parsing:** сохранение заголовков, разделов, пунктов, таблиц, страниц, приложений.

**Chunking:** fixed-size, paragraph, semantic, structure-aware. Для технических и нормативных документов structure-aware обычно предпочтительнее простого окна N токенов.

**Metadata:** `document_id, title, section, page, source, version, date, access_level`.

**Embeddings / Vector search:** запрос и chunks кодируются в векторы, затем выполняется поиск ближайших кандидатов/top-k.

**Hybrid search:** `semantic/vector + lexical/BM25`; особенно полезен для точных номеров, пунктов, артикулов и идентификаторов.

**Reranking:** первичный retrieval даёт кандидатов, reranker повторно сортирует их перед сборкой контекста.

## Grounding & traceability

`Answer → supporting chunk → document section → source version → original source`.

Для регулируемой среды важно также подтвердить актуальность версии и право пользователя на источник.

## Knowledge Graph / GraphRAG

Пример: `Requirement → applies_to → System → protects → Asset → mitigated_by → Control → evidenced_by → Artifact`.

GraphRAG полезен, когда ответ зависит от отношений между сущностями, а не только от похожести текста. Не заявлять глубокую production-компетенцию без реализованного и протестированного контура.

## Контрольные вопросы

1. Чем RAG отличается от fine-tuning?
2. Почему chunk size нельзя выбрать один раз «на глаз»?
3. Зачем hybrid search?
4. Когда reranker не нужен?
5. Как не дать пользователю получить через RAG чужой документ?
6. Что делать, если retrieved chunks релевантны, но ответ модели неверен?
7. Как доказать, что новая embedding model стала лучше?
8. Как обрабатывать новую версию нормативного документа?
9. Чем citation отличается от полной traceability?
10. Когда knowledge graph оправдан, а когда это лишняя сложность?