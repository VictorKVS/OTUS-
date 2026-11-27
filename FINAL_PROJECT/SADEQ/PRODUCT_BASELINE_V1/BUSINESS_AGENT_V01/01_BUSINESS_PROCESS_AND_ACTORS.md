# BPM-001 — бизнес-процесс UAA «событие → проверяемая реакция»
## Участники (BPMN roles in source Mermaid)
| Role | Responsibility | Cannot do |
|---|---|---|
| Business/Data Owner | define value, data scope, business rules, owner of consequences | let model create unauthorized scope |
| Source System | emit signed/authenticated, permitted observations | request unregistered operation |
| UAA B01/B02 | validate, correlate business object, maintain event state | approve business action |
| UAA B03/B04 | collect source evidence, determine hypothesis, calculate options and propose | claim source trust, authorize tool |
| Runtime Policy SEC-04 / B05 | enforce user→agent→tool→object rights and consequences, approve path | rely solely on LLM classification |
| Human Approver | approve exact action+object version+TTL | grant a general unlimited permit via prompt |
| POLYGON SEC-05 | independent exam and trust-version recommendation | edit candidate and approve itself |
| SOC SEC-06 | monitor/revoke/incident | silently change immutable evidence |

## Start event
An approved channel sends a business event, e.g. warehouse stock count observation. Ingress must enforce allowed sender, tenant, size, type, schema version and routing contract.

## Business outcome
A machine-explainable, proven status or a bounded action with a business receipt. If evidence is insufficient, product shall return `REVIEW_REQUIRED` or `ABSTAIN` without unauthorized side effect.

## Two branches
- **Information-only**: event accepted → state updated → threshold not crossed → store audit → done.
- **Consequential**: threshold crossed → evidence → deterministic calculations → proposal → policy → human approval if needed → recheck → idempotent execute → independently verified result → feedback.

## Decision points
1. Sender/schema allowed? No → reject; never merely ignore unknown fields.
2. Object identity unambiguous? No → review; never merge different tenant objects.
3. Significant business change? No → record, no external action.
4. Enough verifiable evidence and algorithm tests? No → abstain.
5. Active agent qualification / permission / impact condition? No → deny.
6. Human approval needed? yes → bind exact params/hash/TTL/object version; reject timeout.
7. State or rights changed after approval? yes → cancel and resubmit.
8. Business receipt matches expected outcome? no → create mismatch/incident, no blind automatic retry.

## Business KPIs (TBD until measured)
- `qualified_results / accepted_events`
- `false_entity_merges / reviewed_matches`
- `abstain_rate`, `human_review_rate`, `median/p95_response_time`
- `cost_per_qualified_result`, `unauthorized_action_count (target zero)`
- `event_replay_consistency`, `audit_completeness`.

## Business invariants
No cloud API in offline MVP; no self-approval; no high-risk autonomous execution. Changes to algorithm/model/data/tool or risk trigger requalification. Threat register from IDEA+ remains continuous through final POLYGON.
