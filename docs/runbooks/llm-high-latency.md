# Runbook — LLM High p95 Latency

Alert: `LLMHighP95Latency`

## Triage

1. Разложить request trace: gateway → retrieval → rerank → model → tools → validation.
2. Проверить TTFT и total model latency.
3. Проверить retrieval latency, queue depth, concurrency and saturation.
4. Проверить provider throttling, retry storms and slow tools.
5. Сопоставить с release/model/index changes.

## Mitigation

- ограничить concurrency / queue;
- применить fallback model/provider;
- отключить/ограничить slow tool;
- уменьшить retrieval/top-k или другой параметр только через контролируемое изменение;
- rollback при regression.

## Exit

p95 вернулся ниже реального SLO threshold, а error/cost/quality не ухудшились как побочный эффект.
