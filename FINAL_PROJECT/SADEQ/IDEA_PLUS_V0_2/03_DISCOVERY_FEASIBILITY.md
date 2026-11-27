# IDEA+ · Prior Art / Internal Scout / Feasibility
## Метод
Сначала проверяем собственные компоненты по исходному коду, контрактам, лицензиям, интеграционным тестам и commit provenance. Затем сопоставляем с известными решениями. Наличие названия сервиса или README не доказывает готовности.
## Технологии-кандидаты
| Нужда | Кандидаты | Необходимый эксперимент |
|---|---|---|
| Agent state / workflow | LangGraph, LlamaIndex Workflows | checkpoint/recovery/branch/approval |
| Local inference | Qwen3 + llama.cpp/Ollama, vLLM/SGLang на Linux | checkpoint license, quant quality, VRAM, KV-cache |
| Vector index | Qdrant, Milvus, Weaviate | ACL, retrieval latency, recovery |
| Knowledge graph | Neo4j | graph traversal, source provenance, tenant boundaries |
| Structured state/events | PostgreSQL | idempotency, transaction, replay |
| Open interfaces | FastAPI/OpenAPI/JSON Schema | contract tests, rate limiting, auth |
| Observability | OpenTelemetry, Prometheus/Grafana, Jaeger | trace audit, sensitive field redaction |
| Security qualification | policy-as-code + independent test suites | bypass attempts + rollback |

## Trade-off
- 20 отдельных агентов: быстро только для первого, далее дублирование, несогласованная безопасность.
- Один огромный prompt: минимальный старт, отсутствуют гарантии состояния/полномочий/тестируемости.
- Shared UAA core + typed specializations: больше стартовых затрат, но проверяемый reuse.
- Cloud LLM API: **не соответствует обязательному air-gapped условию**.

## Состояние проверок на v0.2
INTERNAL_SCOUT = OPEN (нет инвентаризации с подтверждёнными commit/hash/tests); WORLD_SCOUT = CANDIDATES_RECORDED (не завершён экспертный обзор), LICENSE_GATE = OPEN; GPU_SIZING = UNKNOWN; CUSTOMER_DISCOVERY = NOT_STARTED; SECURITY_TESTS = NOT_RUN.

## Feasibility verdict
**RESEARCH / CONDITIONAL_GO только на ограниченный PoC.** Нельзя заявлять промышленную готовность, высокую пропускную способность, подтверждённую стоимость/выгоду или 20 работающих агентов. Первые опровергаемые эксперименты: offline GraphRAG end-to-end; cross-channel identity; User-B security denial; three-specialization incremental hours; load/cost measurements.

## Авторитетные источники для дальнейшей проверки версии и лицензий
- https://docs.langchain.com/oss/python/langgraph/overview
- https://qdrant.tech/documentation/
- https://docs.vllm.ai/
- https://c4model.com/
- https://www.omg.org/spec/BPMN/
- https://www.omg.org/spec/DMN/
- https://www.iiba.org/business-analysis-standards/babok/
- https://www.finops.org/framework/
- https://www.nist.gov/itl/ai-risk-management-framework
- https://owasp.org/www-project-top-10-for-large-language-model-applications/
