# Runbook — LLM Guardrail Spike

Alert: `LLMSecurityGuardrailSpike`

## Triage

1. Определить тип события: prompt injection / sensitive data / unsafe output / policy denial.
2. Не копировать чувствительный prompt/response в обычные tickets/logs.
3. Проверить actor/session/tenant scope через защищённый audit.
4. Проверить изменение model/prompt/policy/tool/index versions.
5. Проверить, были ли tool requests и authorization denials.

## Mitigation

- усилить или включить соответствующий policy/guardrail;
- временно запретить risky tool/path;
- изолировать подозрительный tenant/session при наличии оснований;
- rotate secret только если подтверждено exposure;
- создать incident при критической утечке/unauthorized action.

## Exit

Причина установлена, риск локализован, affected scope известен, corrective action подтверждён тестом/eval.
