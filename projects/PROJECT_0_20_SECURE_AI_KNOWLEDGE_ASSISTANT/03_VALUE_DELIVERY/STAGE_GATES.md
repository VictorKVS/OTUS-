# Stage Gates

## G-DISCOVERY
PASS when:
- source corpus sample exists;
- stakeholders and owner identified;
- REQ/NFR reviewed;
- critical unknowns recorded.

## G-POC
PASS when:
- versioned golden set exists;
- RAG baseline measured;
- known failure classes documented;
- no critical access-control defect.

## G-MVP
PASS when:
- API contract stable enough for integration;
- automated unit/integration tests;
- trace_id throughout request path;
- release artifacts versioned.

## G-PROD-READY
PASS when:
- eval/security regression gates blocking;
- observability/SLO defined;
- capacity test performed;
- rollback drill performed;
- release manifest immutable.

## G-PRODUCTION
PASS when:
- staging passes;
- Canary 1% passes;
- Canary 5% passes;
- 100% promotion passes observation gate.
