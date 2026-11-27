# API-ADR-001 — API-first дизайн SADEQ
## Resource contracts
- **Observation:** исходное неизменяемое наблюдение из конкретного канала, внешний ID, время источника, source/provenance, tenant.
- **Object:** нормализованная сущность, сшивание каналов выполняется с независимой проверкой совпадения и только внутри разрешённого tenant.
- **Event:** нормализованный факт изменения, immutable, source IDs и event-time.
- **AgentProfile:** привязка domain ontology, model, tools allowlist, policies, evaluation version.
- **Run:** исполнение с состоянием / checkpoint и бюджетом шагов.
- **ActionProposal:** черновик действия без права исполнения.
- **QualificationRecord:** аттестация определённой связки artifact hash + model + policies + tools + tenant/domain scope, подпись независимого экзаменатора.

## Политика безопасности
1. Запрашивающий проходит authentication; tenant и scope извлекаются из *проверенного* токена/сессии, а не из свободного поля JSON.
2. Object/Document/Graph Vector ACL проверяется в query layer и при формировании ответа, чтобы исключить боковые утечки из кэша, цитат и логов.
3. Deny by default; principle of least privilege; access decision is auditable and deterministic.
4. ActionProposal создаётся пользователем/агентом, но не вызывает tool.
5. Endpoint `approve` доступен только специально назначенному человеку; статус approval однократный, cryptographically audited.
6. Endpoint `execute` — *только внутренний* service identity tool gateway после проверки policy + approval + version + idempotency key; ни один внешне доступный endpoint не предоставляет execution.
7. Конфликты evidence, ошибочная классификация, нет актуальной аттестации — STOP/ABSTAIN, никогда не override повышением confidence.
8. Rate limit per tenant + caller; trace_id; body and output size limits, safe error responses, no raw model prompt/logging of secrets.
9. Agent cannot change its own policy, tool allowlist, exam corpus, role grants, risk level or release status.

## Versioning & compatibility
Base path `/api/v1`; OpenAPI semantic contract version; backwards compatible additions only inside major version. Breaking changes → /api/v2 + migration + dual-run; `X-Request-ID` and `Idempotency-Key`; timestamps RFC3339 UTC; JSON Schema validation; errors RFC7807-style application/problem+json; asynchronous processing 202 Accepted + poll by resource id.

## EDA interfaces
Ingestion via HTTP for MVP, later broker contracts under AsyncAPI. Event sourcing journal is not an event bus. Delivery guarantees need idempotency and outbox; end-to-end exactly-once is **not** promised without evidence.

## API as a product
Consumer personas, ownership per route, SDK docs, sandbox mocks, SLA/SLO, quotas, deprecation, support and telemetry. Cost per request: API processing + retrieval + LLM tokens + storage + audit + qualification. API latency and LLM latency are different metrics.

## OTUS acceptance
OpenAPI lint and schema valid, security negative tests (User B, old version, fake approval, missing scope, replay action, malicious source), trace to FR/TEST/ADR, documented limits and sample request. This v0.1 is **only source specification**, not a verified API implementation.
