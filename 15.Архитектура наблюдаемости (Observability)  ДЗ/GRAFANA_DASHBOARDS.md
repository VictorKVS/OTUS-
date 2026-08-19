# Grafana dashboards для AI-систем

Каталог Grafana содержит готовые community dashboards для разных источников данных, включая Prometheus, Loki, Tempo, PostgreSQL, Elasticsearch, OpenSearch, CloudWatch, Azure Monitor и Kubernetes. Готовый dashboard следует рассматривать как стартовый пример: перед production необходимо проверить запросы, происхождение, плагины, права доступа и соответствие своей схеме метрик.

## Рекомендуемые экраны

### 1. Executive / SLO

- availability и error budget;
- p50/p95/p99 latency;
- успешность запросов;
- стоимость за день и месяц;
- число security/safety incidents.

### 2. LLM runtime

- requests/sec и concurrent requests;
- input/output tokens;
- time to first token и total latency;
- ошибки провайдера, timeout и retry;
- стоимость по модели, endpoint и продукту.

### 3. RAG

- retrieval latency;
- количество найденных чанков;
- Recall@k и Precision@k на eval-наборе;
- доля ответов с корректными citations;
- пустая выдача, ACL denial и cross-tenant anomaly.

### 4. Agents

- tool calls на запрос;
- success/error/denied по инструментам;
- количество циклов агента;
- human approvals;
- действия, остановленные policy engine.

### 5. Security

- prompt-injection detections;
- sensitive-data blocks;
- abnormal token/cost spikes;
- unsafe output handling;
- изменения моделей, индексов и политик.

## Правила проектирования

- начинать с вопроса пользователя dashboard, а не с доступных графиков;
- отображать SLO и пороги рядом с фактическими значениями;
- связывать метрики, логи и трейсы общим `trace_id`;
- избегать высокой cardinality в labels;
- задавать владельца и runbook для каждого алерта;
- версионировать JSON dashboard в Git;
- скрывать секреты и персональные данные;
- проверять dashboard на нормальном, деградированном и аварийном сценариях.

## Импорт примера

1. Открыть Grafana → Dashboards → New → Import.
2. Загрузить `grafana/llm-observability-dashboard.json`.
3. Выбрать Prometheus datasource.
4. Сопоставить имена метрик со своим exporter.
5. Проверить панели и пороги на тестовой нагрузке.
