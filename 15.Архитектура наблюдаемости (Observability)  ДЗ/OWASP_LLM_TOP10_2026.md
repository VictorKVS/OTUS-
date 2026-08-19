# OWASP GenAI LLM Top 10 2026

Актуальная редакция опубликована в августе 2026 года. Старая страница OWASP теперь является архивной точкой входа; канонический материал развивается в OWASP GenAI Security Project.

| ID | Риск | Что наблюдать |
|---|---|---|
| LLM01 | Prompt Injection | срабатывания input/output guardrails, подозрительные инструкции, смена tool path |
| LLM02 | Sensitive Information Disclosure | DLP-события, секреты/PII в выводе, необычные объёмы ответа |
| LLM03 | Excessive Agency | число и тип tool calls, отказ авторизации, действия без подтверждения |
| LLM04 | Supply Chain | версии моделей и библиотек, provenance, результаты SCA/SBOM и проверки артефактов |
| LLM05 | Data and Model Poisoning | drift, аномалии качества, происхождение данных, изменения датасетов и индекса |
| LLM06 | Unbounded Consumption | tokens/request, cost/request, concurrency, очереди, timeout и rate-limit |
| LLM07 | Misinformation | groundedness, factuality, human overrides, жалобы и провалы eval |
| LLM08 | Hidden Context Exposure | утечки system prompt/context, необычные цитаты внутренних инструкций |
| LLM09 | Vector and Embedding Weaknesses | retrieval precision/recall, cross-tenant hits, ACL denials, аномальные similarity scores |
| LLM10 | Improper Output Handling | блокировки unsafe output, ошибки парсинга, попытки injection в downstream-системы |

## Правило применения

OWASP Top 10 — не готовая модель угроз и не контрольный список соответствия. Для каждого проекта риски связываются с активами, потоками данных, угрозами, контролями, владельцами, тестами и процедурами реагирования.

## Минимальные события аудита

- `request_received` — без сохранения чувствительного текста по умолчанию;
- `guardrail_triggered`;
- `retrieval_completed` с разрешёнными `source_id`;
- `model_invoked` с моделью, токенами и задержкой;
- `tool_requested`, `tool_authorized`, `tool_completed`;
- `output_validation_failed`;
- `human_approval_requested`;
- `incident_created`.

## Безопасность самой телеметрии

- применять минимизацию и маскирование данных;
- разделять технические метрики и защищённый аудит;
- ограничивать доступ к логам по ролям;
- устанавливать сроки хранения;
- защищать целостность и синхронизацию времени;
- не использовать prompt или response как label метрики.
