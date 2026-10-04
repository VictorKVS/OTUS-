# Runbook — LLM High Error Rate

Alert: `LLMHighErrorRate`

## Signal

Error rate превышает учебный threshold из `prometheus/llm-alerts.yml`.

## Triage

1. Проверить scope: provider / endpoint / model / release.
2. Сопоставить рост ошибок с deploy/config/model/prompt/index changes.
3. Проверить timeout/retry/rate-limit/provider errors.
4. По trace ID найти failing spans.
5. Проверить dependency health и очереди.

## Mitigation

- rollback последнего изменения при подтверждённой связи;
- переключить fallback/provider/model route, если предусмотрено;
- снизить traffic / concurrency при saturation;
- отключить проблемный tool/integration через policy, если источник ошибок там.

## Evidence to save

- alert start/end;
- affected SLI/SLO;
- release/model/prompt/index versions;
- trace examples;
- mitigation;
- owner;
- incident/RCA link.

## Exit

Error rate вернулся в SLO и остаётся стабильным на согласованном observation window.
