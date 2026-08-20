# KEDA: событийное масштабирование AI-нагрузки

KEDA — лёгкий Kubernetes-компонент для event-driven autoscaling. Он работает вместе со стандартным Horizontal Pod Autoscaler и масштабирует выбранные workloads по внешним источникам событий и метрикам.

## Где применять в AI-системе

- очередь запросов на batch inference;
- Kafka/RabbitMQ/NATS/Redis Stream с заданиями;
- очередь обработки документов и embeddings;
- асинхронная генерация изображений;
- пайплайн eval и post-processing;
- Prometheus-метрика queue lag или request backlog;
- Kubernetes Job для дискретных заданий.

## Выбор сигнала

CPU/GPU utilization — запаздывающий сигнал. Для очередей полезнее масштабироваться по backlog, lag и времени ожидания:

- `target_backlog_per_worker`;
- `pending_messages`;
- `consumer_lag`;
- `oldest_message_age`;
- `requests_in_flight`;
- `estimated_queue_time`.

## Упрощённый расчёт

```text
processing_rate_per_worker = 1 / average_processing_time
required_workers = ceil(arrival_rate / processing_rate_per_worker / target_utilization)
estimated_wait = pending_events / (workers × processing_rate_per_worker)
```

Для GPU inference дополнительно учитываются batch size, VRAM, model replicas, время загрузки модели и лимит одновременных запросов.

## Параметры настройки

- `minReplicaCount` — базовая доступность и защита от cold start;
- `maxReplicaCount` — квоты, GPU и бюджет;
- polling interval — частота проверки источника;
- cooldown period — защита от частых scale-down;
- activation threshold — когда workload просыпается с нуля;
- target value — нагрузка на одну реплику;
- fallback — безопасное число реплик при недоступности метрик.

## Quality gates

- scaler имеет только необходимые права;
- секреты источника событий не находятся в manifest открытым текстом;
- max replicas согласован с квотами и бюджетом;
- метрики scaler доступны в observability;
- нагрузочный тест проверяет burst, sustained load и падение источника метрик;
- не происходит oscillation или чрезмерного scale-up;
- graceful shutdown завершает активные задания;
- DLQ и retry не создают бесконечный шторм событий.

## Комбинация с Semantic Cache

Сначала кеш уменьшает фактический поток в LLM. KEDA должна видеть очередь после кеша, иначе система будет масштабироваться по запросам, которые могли быть обслужены без инференса. Для синхронного low-latency пути обычно сохраняют минимальное число прогретых реплик; scale-to-zero оставляют асинхронным workload.
