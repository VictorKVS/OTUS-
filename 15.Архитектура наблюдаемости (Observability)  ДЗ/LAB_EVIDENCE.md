# Lesson 15 — Alerting Lab Evidence

Статус: **VERIFIED FROM PROVIDED ARCHIVE**

Архив: `alerting-373402-178176.tgz`

## Что подтверждено внутри

Демонстрационный стенд содержит:

- FastAPI ML inference service;
- Prometheus metrics;
- Kubernetes Deployment / Service / ServiceMonitor;
- kube-prometheus-stack usage;
- Grafana dashboard JSON;
- load test;
- Mermaid dataflow and Kubernetes topology;
- readiness/liveness probes;
- intentional error and latency injection for degraded-state testing.

Ключевые метрики demo:

- `prediction_requests_total`;
- `prediction_errors_total`;
- `prediction_latency_seconds`;
- generic HTTP request metrics from instrumentation.

Dashboard archive показывает:

- Error Rate;
- p95 Latency;
- HTTP Throughput.

## Что этот стенд доказывает

Он является практическим evidence для классической части observability:

`SERVICE → /metrics → ServiceMonitor → Prometheus → Grafana → Alerting`

и позволяет воспроизводимо проверить normal/degraded/failure behaviour.

## Что он НЕ доказывает

Стенд не является полным LLM/RAG/Agent observability stack:

- нет RAG retrieval/eval telemetry;
- нет tokens/cost/model-provider metrics;
- нет guardrail / prompt-injection events;
- нет agent tool traces;
- нет production IAM/secrets configuration.

Поэтому он используется как **lab evidence**, а LLM-specific target architecture определяется отдельными manifest/dashboard/alert artifacts Lesson 15.

## Security note

В demo README используется учебный Grafana password `admin`. Это допустимо только для локального demo и не является production practice.
