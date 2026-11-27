# ТП-001 — Информационные контракты и границы данных
**Статус:** DESIGN / NOT_IMPLEMENTED / NOT_TESTED. **Конвенция:** RFC 8259 JSON, JSON Schema Draft 2020-12; timestamp — RFC 3339 (format assertion enabled in validator), SHA-256 hex lowercase.

## 1. Проектные контракты
| FLOW | Место | Версия | Содержимое | Права и ограничения |
|---|---|---|---|---|
| FLOW-01 | mock ITSM → B01 | `InboundIncidentV1` | request_id, external_ticket_id, source_system, service_key, priority, kind, summary, indicators, timestamp | untrusted body, no tenant/role/principal; reject additionalProperties, length, enum violations |
| FLOW-02 | B01 → B02 | `ValidatedObservationV1` | trusted tenant/principal, normalized object ref, idempotency digest, source hash, trace | schema applies only to internal trusted producer B01; cannot be directly submitted by client |
| FLOW-06 | B04 → B05 | `ActionProposalV1` | exact ticket/status, source citations, state version, expiry | proposal is NOT a permission; no arbitrary tool URL/SQL/shell |
| FLOW-07 | Approver → B05 | `ApprovalDecisionV1` | proposal UUID, digest, decision, reason, state version | principal + role from server authentication; approve only immutable canonical proposal |
| FLOW-08 | B05 → adapter | `AuthorizedToolCallV1` | **TBD dedicated schema and signed scoped token** | B05-only, not directly exposable to model or user |
| FLOW-09 | adapter → B05 | `AuthoritativeObjectStateV1` | **TBD dedicated schema** | must read back external system state, not trust 200 alone |

## 2. Правила обработки и сериализации
1. B01 uses auth middleware with verified tenant_id, principal_id, roles, permitted source and destination. Request body may not supply these.
2. Select schema by **server-registered** `source_system + schema_version`, authenticate channel first; reject unknown keys throughout all nested objects; reject malformed UTF-8, oversize body, type mismatch, invalid dates, duplicate JSON member names (decoder policy).
3. Validating JSON schema alone **is not authentication**; also enforce source authorization, anti-replay, rate limiting and resource bounds.
4. Normalize source record, compute `source_sha256` from an exact declared canonical serialization. For initial fixture, use `json.dumps(... sort_keys=True, separators=(",", ":"), ensure_ascii=False)` UTF-8 in Python; **not** a language-neutral canonicalization standard, needs ADR before cross-language deployment.
5. Server constructs `ValidatedObservationV1`; never forward arbitrary extra user fields. Internal event id is UUID generated server-side. `tenant_id` solely verified identity, checked on every read/write.
6. B04 produces an `ActionProposalV1` with exact expected postcondition, citations from authorized KB, no access token. Check `arguments.new_status == expected_postcondition.status` as **semantic rule outside JSON schema**.
7. B05 saves immutable canonical proposal and computes its digest; approver decision refers to exact hash. Verify identity, tenant, role, expiry, current state, tool allowlist and proposal status **again immediately before execution**.
8. Reject stale schema or mismatched versions by explicit error; never deserialize unknown model-generated fields into a privileged object.

## 3. Known limitations before implementation
- JSON Schema enum and `additionalProperties:false` enforce shape, not **identity, object tenancy, permissions, atomic idempotency, execution or answer accuracy**.
- `format: date-time`/UUID requires validator configured with FormatChecker. UTC normalization and ordering need application code.
- `tenant_id` exists in the internal validated observation and proposal but is verified **against the trusted tenant**.
- Proposal digest must bind canonical JSON bytes, version, expiry, target object/state, tool and arguments; digest alone is not proof of approval.
- Negative fixture spoofing tenant in `InboundIncidentV1` must fail schema validation, rather than silently trusting user value.
- Approved evidence is valid only for the authorized query context; prompt content is untrusted and cannot change route permissions.

## 4. Error contracts (proposed)
`UNAUTHENTICATED` (401), `FORBIDDEN_SOURCE` (403), `CONTRACT_INVALID` (422), `CONFLICT_DUPLICATE` (409 if conflicting payload under same idempotency key), `REVIEW_REQUIRED` (409), `APPROVAL_REQUIRED` (202), `APPROVAL_STALE` (409), `POLICY_DENIED` (403), `EXECUTION_UNKNOWN` (202 + reconciliation), `OUTCOME_MISMATCH` (409). These are design semantics, not implemented HTTP responses.

## 5. Implementation interfaces
First endpoint `POST /incidents`. Later `POST /documents`, `POST /queries`, `POST /proposals/{id}/decision`, `GET /audit/{trace_id}`. All are tentative until published OpenAPI 3.1 and component owner review.
