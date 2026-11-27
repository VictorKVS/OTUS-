# BUSINESS-CASE-001 — Склад: мало товара → рекомендация заказа
**All example values synthetic. No production metrics or executed tests.**
## Step-by-step input
1. Tenant **TENANT-A**, approved source ERP emits count observation `sku-25` at time T1: **14 units**.
2. Same verified source at T2 emits count observation `sku-25`: **9 units**.
3. Approved business rule for example: `reorder_point = 10 units`. This number is **not a recommendation for real stock**, just deterministic sample input.
4. Authoritative object registry yields identical `object_id` for both, never across tenant boundary.

## Calculations and algorithm IDs
- ALG-01 verifies authenticated source and closed schema; ID and `stock_count` type nonnegative integer.
- ALG-02 dedupe by tenant/source/event ID, no repeated side effect.
- ALG-03 resolves same canonical object by exact source mapping.
- ALG-04 appends two immutable observations with SHA + provenance.
- ALG-05 projects version 1 as `stock_count=14`, version 2 as `stock_count=9`; reproducible from event log.
- ALG-06 computes delta `9 - 14 = -5`; threshold trigger `9 < 10` -> significant change.
- ALG-07 retrieves authorised procurement policy and recent orders (if available), cited and tenant scoped.
- ALG-08 indicates hypothesis «inventory below reorder point» as **rule-evidenced fact**, not inferred causal reason for decline; causes remain unknown unless supported.
- ALG-09 forecast `NOT_AVAILABLE` because two points insufficient for production-quality forecast; does not invent predicted demand.
- ALG-10 DMN example: stock below reorder point + procurement policy available -> `DRAFT_REORDER_SUGGESTION`, otherwise `REVIEW_REQUIRED`.
- ALG-11 policy: `draft.create` may be allowlisted low-risk, `purchase_order.submit` requires human approval. Neither LLM nor validation automatically performs financial purchase.
- ALG-12 checks that draft with expected SKU and count is created in the authorised system and writes audit; false receipt → MISMATCH/INCIDENT.

## Contract examples
```json
{"source_id":"ERP-A","schema_version":"stock_count.v1","external_event_id":"evt-002","external_key":"sku-25","observed_at":"2026-11-27T14:00:00Z","payload":{"stock_count":9}}
```

### Proposed result (not system output)
```json
{
  "object_id": "OBJECT-25",
  "state_version": 2,
  "change": {"old_stock":14,"new_stock":9,"delta":-5,"reorder_point":10},
  "decision": "PROPOSE_DRAFT_REORDER",
  "execution_status": "NOT_EXECUTED",
  "forecast_status": "NOT_AVAILABLE",
  "evidence": ["EVENT-001","EVENT-002","PROCUREMENT-RULE-001"]
}
```
Final schemas must clarify identity propagation and `additionalProperties: false` at every nested level, so this result is illustrative, not contract-approved.

## Negative scenarios
Source unknown field; forged role; source tenant mismatch; duplicate evt-002; different tenant same sku-25; negative count; out-of-order updates; expired procurement policy; absent rule source; human reject; changed stock count after approval; tool receipt not found.
