# Матрица наблюдаемости LLM

| Область | Метрика | Лог/событие | Trace span | Алерт |
|---|---|---|---|---|
| Доступность | `llm_requests_total`, `llm_errors_total` | provider error | `model.invoke` | error rate > SLO |
| Задержка | `llm_request_duration_seconds` | timeout/retry | request → retrieval → model → tools | p95 выше порога |
| Стоимость | `llm_input_tokens_total`, `llm_output_tokens_total`, `llm_cost_total` | budget event | `model.invoke` attributes | резкий рост cost rate |
| RAG | `rag_retrieval_duration_seconds`, `rag_empty_results_total` | selected source IDs | `retrieval`, `rerank` | empty-result spike |
| Grounding | `llm_grounded_responses_total` | citation validation | `output.validate` | groundedness ниже порога |
| Prompt injection | `llm_guardrail_triggers_total{type="prompt_injection"}` | redacted detection event | `guardrail.input` | всплеск атак |
| Sensitive data | `llm_guardrail_triggers_total{type="sensitive_data"}` | DLP block | `guardrail.output` | любая критическая утечка |
| Agency | `agent_tool_calls_total`, `agent_tool_denied_total` | authorization decision | `tool.authorize`, `tool.execute` | denied/spike/anomalous tool |
| Consumption | `llm_tokens_per_request` | rate-limit event | full request | token или concurrency spike |
| Supply chain | `model_info`, `component_vulnerability_total` | deployment/SBOM event | deployment trace | неизвестная версия/CVE |

## RED + USE + AI

- RED: Rate, Errors, Duration для запросов.
- USE: Utilization, Saturation, Errors для CPU/GPU/памяти/очередей.
- AI: Tokens, Cost, Quality, Retrieval, Safety и Agency.

## Три уровня проверки

### Минимум

Метрики запросов, ошибок, задержки и токенов; один dashboard; два алерта.

### Рабочий уровень

Metrics + logs + traces, RAG и agent panels, security events, runbooks.

### Продвинутый уровень

SLO/error budgets, автоматические eval, tenant isolation, drift, cost anomaly detection и корреляция с релизами.
