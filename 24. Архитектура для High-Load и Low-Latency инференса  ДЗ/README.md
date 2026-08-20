# Урок 24. High-Load и Low-Latency инференс

Дополнительные материалы связывают два механизма оптимизации:

1. **Semantic Cache** уменьшает число повторных вызовов LLM, задержку и стоимость.
2. **KEDA** масштабирует Kubernetes-обработчики по реальному потоку событий и внешним метрикам.

## Архитектурный конвейер

```text
Client
  → API Gateway / rate limit
  → Semantic Cache lookup
      → HIT: validated cached answer
      → MISS: queue / inference router
          → KEDA scaler
          → inference workers / GPU pool
          → response validation
          → cache write
  → metrics, tracing and cost accounting
```

## Основные вычисления

- `cache_hit_rate = cache_hits / total_cache_lookups`
- `effective_llm_rps = incoming_rps × (1 - cache_hit_rate)`
- `saved_llm_calls = total_requests × cache_hit_rate`
- `average_latency = hit_rate × cache_latency + miss_rate × inference_latency`
- `required_workers = ceil(arrival_rate × processing_time / target_utilization)`
- `queue_lag_seconds = pending_events / processing_rate`

## Quality gates

- кэш не возвращает ответ ниже порога semantic similarity;
- ключ кеша учитывает контекст, tenant, модель, версию prompt и политики безопасности;
- персональные и конфиденциальные данные не смешиваются между пользователями;
- autoscaling не нарушает GPU/CPU-квоты и бюджет;
- p95/p99 latency, error rate, queue lag и cost/request находятся в пределах SLO;
- scale-to-zero применяется только там, где cold start совместим с latency SLO.

## Файлы

- [SEMANTIC_CACHE.md](SEMANTIC_CACHE.md)
- [KEDA_AUTOSCALING.md](KEDA_AUTOSCALING.md)
- [SOURCES.md](SOURCES.md)
