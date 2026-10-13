# Requirements Traceability Matrix · Wave 1

| Business / Risk | Requirement | Architecture | Verification |
|---|---|---|---|
| user needs confirmed answer | FR-005/006/007 | Retrieval → Context → Output Validator | golden-set eval |
| prevent cross-scope leakage | FR-002/003, R-002 | Identity + Policy before Retrieval | ACL adversarial test |
| reproducible release | FR-012, R-005 | Release Manifest / Registry | manifest schema validation |
| safe rollout | FR-013/014, R-007 | Canary + stable retained | rollback drill |
| measurable performance | NFR-PERF-* | API/Model/Obs planes | load test |
| grounded quality | NFR-QLT-* | RAG + eval service | RAGAS/DeepEval + human review |
| no invented thresholds | R-008 | provenance labels | architecture review |
