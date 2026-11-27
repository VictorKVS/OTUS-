# API Contract and Security Acceptance — v0.1
| ID | Test | Expected result |
|---|---|---|
| API-T01 | POST observation with valid Idempotency-Key | 202 + stable observation_id |
| API-T02 | repeat same key and same body | same result, no duplicate event/action |
| API-T03 | repeat key with different body | 409 conflict |
| API-T04 | B requests object from A | 404/403 (consistent anti-enumeration policy), audit no secret leakage |
| API-T05 | create action proposal | 201 PROPOSED; **tool not called** |
| API-T06 | approve action with agent token | 403; no status change |
| API-T07 | approve with human permission | APPROVED, attributable identity |
| API-T08 | expired qualification used for action | DENY |
| API-T09 | conflict in evidence / civilian object high risk | ABSTAIN, no tool call |
| API-T10 | prompt injection in observation payload | text treated as data; cannot override system policy |
| API-T11 | orphan event or cross-tenant object link | validation or policy rejection |
| API-T12 | invalid JSON / unbounded body | 400/413 and redacted logs |
| API-T13 | no route to Internet in final OTUS | egress blocked; complete request handled locally |
| API-T14 | change model or tool allowlist | existing qualification invalidated; requalification required |
| API-T15 | rate limits and p95 latency | measured and documented separately for API/retrieval/LLM |

**Independent examiner:** SEC-05 owns acceptance and test fixtures; candidate programming agent must not rewrite qualification tests. Evidence must contain versioned source commit, results and runtime environment. No tests executed at design stage.

## Build sequence
1. Run OpenAPI schema validator and diff checker.
2. Generate a deterministic mock and sample fixtures.
3. Implement PostgreSQL event store + idempotency.
4. Implement server-side JWT validation / ACL / tenant boundaries.
5. Wire local GraphRAG with citations and retrieval scope.
6. Wire LangGraph / stateful agent run.
7. Create deterministic policy enforcement for ActionProposal.
8. Run independent abuse/security tests.
9. Collect performance traces and actual TCO.

## Release gate
No API exposure as production until functional, ACL, audit, failure cases, offline and qualification tests have passed and been reviewed.
