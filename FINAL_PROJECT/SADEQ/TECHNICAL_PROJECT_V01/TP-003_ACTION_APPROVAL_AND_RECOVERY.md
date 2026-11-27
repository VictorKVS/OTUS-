# ТП-003 — Безопасное предложение, согласование и подтверждение действия
**Статус:** DESIGN / TESTS NOT RUN.

## 1. Deterministic approval state machine
`DRAFT → POLICY_CHECKED → APPROVAL_PENDING → APPROVED → REVALIDATING → EXECUTING → VERIFYING → VERIFIED`.
Other terminal outcomes: `DENIED`, `REJECTED`, `EXPIRED`, `STALE`, `EXECUTION_UNKNOWN`, `MISMATCH`. `EXECUTION_UNKNOWN` **not** automatically terminal until reconciled. State transitions require actor and eligible prior state; no arbitrary jumps.

## 2. Tool allowlist
P0 permits **only** `mock_itsm.update_ticket_status`, with `new_status ∈ {IN_PROGRESS, WAITING_FOR_SUPPORT}`; no shell, arbitrary HTTP request, DB mutation, real system access. LLM produces proposal data, not tool credentials. `ActionProposal` target ticket and tenant must match authorized identity and existing B02/ITSM record.

## 3. Exact approval binding
1. Save immutable proposal and generate `proposal_sha256` using defined canonical representation.
2. Show approver: tenant, target ticket, previous state/version, new state, reason, evidence references, expiry and action hash.
3. Authentication must come from trusted session. Check role and tenant on each approval, reject operator self-approval if segregation-of-duties policy requires it.
4. Compare signed or otherwise authenticated decision to current proposal digest and state version. Reject repeated decision or expired/stale decision.
5. Before execution re-evaluate rights, allowed tool, account, source validity, object state/version, TTL; deny if any component changed.
6. Generate scoped service-to-service authorization only inside B05 tool adapter; credentials never enter B04/prompt context.

## 4. Side effect and reconciliation
- Persist execution intent and idempotency token in transaction, then invoke mock ITSM with token. ITSM adapter must support idempotent effect keyed by token.
- If response returns success, perform independent read-after-write through authorized read endpoint; compare `status` and target ticket.
- If timeout/network failure after send, mark `EXECUTION_UNKNOWN`, **query ITSM state first** before any retry. Never assume failure merely because transport timed out.
- Mismatch causes incident and manual resolution; do not mark `VERIFIED`, and do not send a blind second mutation.
- Persist receipt, audit and evidence with redaction, including exact versions. Release POLYGON cannot be bypassed by agent.

## 5. Negative cases
| ID | Attack/failure | Required output |
|---|---|---|
| T-ACT-001 | model proposes unregistered tool | CONTRACT_INVALID / DENY |
| T-ACT-002 | proposal tenant B for principal A | POLICY_DENIED |
| T-ACT-003 | expired approval / changed action digest | APPROVAL_STALE |
| T-ACT-004 | mismatching state_version | STALE (no tool call) |
| T-ACT-005 | injection in SOP tries `admin_export_all` | no tool emitted, adversarial trace |
| T-ACT-006 | timeout after state mutation | EXECUTION_UNKNOWN → verified by read, no repeated mutation |
| T-ACT-007 | HTTP 200 with unchanged state | MISMATCH |
| T-ACT-008 | candidate tries self-qualification | forbidden and logged |
