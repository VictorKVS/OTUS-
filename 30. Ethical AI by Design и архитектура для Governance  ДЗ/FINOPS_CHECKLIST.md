# FinOps checklist для AI/LLM-системы

## Inform

- [ ] Определён FinOps scope: продукт, среда, cost center и владелец.
- [ ] Затраты распределяются по модели, API, GPU, storage, network и команде.
- [ ] Считаются cost/request, cost/1K tokens и cost/successful outcome.
- [ ] Есть своевременные и точные отчёты, budget, forecast и anomaly alerts.
- [ ] Метрики качества и безопасности отображаются рядом со стоимостью.

## Optimize

- [ ] Сравнены API, self-hosted и hybrid варианты.
- [ ] Проверены model size, quantization, batching и routing.
- [ ] Настроены semantic/prompt cache и контроль ложных попаданий.
- [ ] Используются autoscaling, schedules и удаление idle-ресурсов.
- [ ] Проверены commitments/discounts без избыточной фиксации.
- [ ] Каждая экономия подтверждена замером качества, latency и риска.

## Operate

- [ ] Назначены Engineering, Finance, Product, Security и Procurement roles.
- [ ] Установлены budget gates для dev/stage/prod.
- [ ] Есть автоматические действия при аномалиях и ручное подтверждение опасных изменений.
- [ ] Проводится ежемесячный review unit economics и архитектурных решений.
- [ ] Решения и результаты заносятся в ADR/Model Card/changelog.

## Формулы

- `cost_request = total_ai_cost / requests`
- `cost_success = total_ai_cost / successful_business_outcomes`
- `token_cost_share = token_cost / total_service_cost`
- `waste_rate = idle_or_unused_cost / total_cost`
- `forecast_error = abs(actual - forecast) / actual`
