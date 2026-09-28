# AI Agents & Secure AI Interview Playbook

## Agent

Agent — программная система, где модель участвует в выборе следующего действия, использует разрешённые инструменты и меняет состояние задачи до цели или stop condition.

`Goal → Observe → Decide → Allowed Tool → Execute → Validate → Continue/Finish`.

LLM не должна иметь неограниченный прямой доступ к ОС, БД или корпоративным системам.

## Multi-Agent

Разделение оправдано, когда различаются роли, permissions, tools, context, модели, критерии качества или ответственность. Если один deterministic workflow решает задачу надёжно, multi-agent не нужен.

## Orchestration

Orchestrator отвечает за routing, state, retries, timeout, error paths, human approval и audit. Важно различать LLM decision, state-machine/workflow decision и application policy.

## Memory

Short-term — текущий контекст; working state — состояние workflow; long-term — долговременные факты/история, если хранение разрешено. Long-term memory требует lifecycle, access control и обновления/удаления.

## MCP

`Agent/LLM app → MCP client → MCP server → Tools/Resources`.

MCP унифицирует интеграции, но сам по себе не решает auth, authorization, validation и audit.

## Prompt injection

Direct — пользователь пытается изменить инструкции. Indirect — внешние данные содержат инструкции для модели. Правило: retrieved/external content — данные, а не доверенные system instructions.

## Data leakage

В enterprise RAG authorization должна происходить до retrieval: `Identity → Roles/Claims → Allowed sources/docs/chunks → Retrieval → Context → LLM`.

## Tool security

Для tool нужны allowlist, input schema, authn/authz, least privilege, safe defaults, timeout, approval для опасных действий и audit log.

## Guardrails

Guardrails — слои контроля: input validation, policy checks, retrieval authorization, tool permissions, schema validation, rate/cost limits, output verification и monitoring.

## Human-in-the-loop

Нужен для удаления/изменения данных, внешних сообщений, юридически или финансово значимых действий, изменения прав, публикации чувствительного результата и других операций с высокой ценой ошибки.

## Контрольные вопросы

1. Чем agent отличается от обычного workflow?
2. Где должна жить authorization — в prompt или в приложении?
3. Почему MCP не делает tool безопасным автоматически?
4. Как защищаться от indirect prompt injection?
5. Как ограничить destructive action?
6. Какая память нужна агенту?
7. Почему десять агентов могут быть хуже одного?
8. Что обязательно логировать?
9. Где нужен human-in-the-loop?
10. Как отделить решение модели от обязательной policy?