# ТП-002 — Модель объекта, дедупликации, событий и состояния
**Статус:** DESIGN / NO DATABASE INSTALLED OR TESTED.

## 1. Business object identity
Identity tuple for P0 `(trusted_tenant_id, source_system, external_ticket_id)`, with server-assigned `object_id UUID`. Cross-tenant identity never merged. `service_key` points to related asset but is **not** the ticket primary identity. Fuzzy entity resolution is explicitly out of P0; ambiguity → REVIEW_REQUIRED.

## 2. Idempotency and transaction boundaries
`idempotency_key = SHA256(tenant_id || 0x1F || source_system || 0x1F || request_id)`; hash input is UTF-8 with delimiters, not client-controlled tenant ID. **Must also store request_payload_digest** and reject reuse of same key with different canonical payload. Unique DB constraint on `(tenant_id, idempotency_key)`. Concurrency semantics:
1. Begin transaction.
2. Insert `receipt` with unique constraint and payload digest; when conflict, lock/read existing record and compare digest.
3. Resolve or create canonical object under `(tenant, source_system, external_ticket_id)`.
4. Append immutable event and transactional outbox record **within same transaction**, guarded by incoming idempotency receipt.
5. Commit. Emit side effects **only asynchronously** after atomic commit; repeated requests reuse receipt. Don't call external tool inside ingest DB transaction.

## 3. Minimal relational design
```sql
CREATE TABLE ticket_object (
 object_id UUID PRIMARY KEY,
 tenant_id TEXT NOT NULL,
 source_system TEXT NOT NULL,
 external_ticket_id TEXT NOT NULL,
 state_version BIGINT NOT NULL DEFAULT 0,
 state_hash CHAR(64),
 UNIQUE(tenant_id, source_system, external_ticket_id)
);
CREATE TABLE ingest_receipt (
 tenant_id TEXT NOT NULL,
 idempotency_key CHAR(64) NOT NULL,
 request_digest CHAR(64) NOT NULL,
 event_id UUID,
 created_at TIMESTAMPTZ NOT NULL,
 PRIMARY KEY(tenant_id, idempotency_key)
);
CREATE TABLE object_event (
 event_id UUID PRIMARY KEY,
 tenant_id TEXT NOT NULL,
 object_id UUID NOT NULL REFERENCES ticket_object(object_id),
 seq BIGINT NOT NULL,
 event_type TEXT NOT NULL,
 source_ref TEXT NOT NULL,
 payload_digest CHAR(64) NOT NULL,
 observed_at TIMESTAMPTZ NOT NULL,
 ingested_at TIMESTAMPTZ NOT NULL,
 UNIQUE(tenant_id, object_id, seq)
);
CREATE TABLE event_outbox (
 outbox_id UUID PRIMARY KEY,
 event_id UUID NOT NULL UNIQUE REFERENCES object_event(event_id),
 dispatch_state TEXT NOT NULL DEFAULT 'PENDING'
);
```
**Further LLD required:** composite tenant FK enforcement / RLS policy, append-only permissions, receipt lifecycle, event body storage with encryption/retention, outbox retries, uniqueness + advisory locking/sequence concurrency, temporal corrections, partitions, recovery/backup.

## 4. State reducer and ordering (ALG-05)
`reduce(state, event) -> new_state` must be deterministic for pinned algorithm version. Event order is **per-object persisted sequence**, not client timestamps. A late event is appended with its own source timestamp and new sequence; if it represents correction, carry explicit `CORRECTION` semantics, don't silently rewrite history. State hash is computed on canonical application representation; replay from initial snapshot and ordered events must reproduce same semantic state and digest. Any version mismatch requires review/retry, not blind overwrite.

## 5. Trigger algorithm (ALG-06)
First policy: emit `NEEDS_ANALYSIS` when new/changed `INCIDENT` is not resolved and authorized evidence inquiry exists; otherwise `NO_ACTION` with trace. Real operational priorities from service catalog MAT-01 and service owner, not LLM's invented threshold.

## 6. Acceptance tests
- T-OBJ-001 same request ID + same body ⇒ one event and same receipt.
- T-OBJ-002 same request ID + different body ⇒ conflict, no extra event.
- T-OBJ-003 same external ticket ID, different tenant ⇒ two separate objects.
- T-OBJ-004 100 concurrent duplicate inputs ⇒ one business event (target, not tested).
- T-OBJ-005 replay and restart ⇒ same state hash.
- T-OBJ-006 late event/correction ⇒ explicit new state version, no retroactive deletion.
- T-OBJ-007 DB transaction rollback ⇒ no partial event/outbox writes.
