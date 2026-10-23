# Risk Register

Scale: Probability 1–5 × Impact 1–5. Score is prioritization, not probability theory.

| ID | Category | Risk | P | I | Score | Response | Trigger |
|---|---|---|---:|---:|---:|---|---|
| R-001 | Data | poor PDF/scanned quality breaks ingestion | 4 | 4 | 16 | OCR quality sample + fallback/manual lane | extraction below approved quality |
| R-002 | Security | retrieval bypasses ACL | 3 | 5 | 15 | policy filter before retrieval + adversarial tests | first forbidden hit |
| R-003 | Quality | model answers beyond evidence | 4 | 5 | 20 | grounded prompt + abstain + faithfulness gate | eval regression |
| R-004 | Data | stale document remains canonical | 3 | 4 | 12 | source versioning + validity metadata | conflicting version found |
| R-005 | Ops | app release references wrong model/index | 3 | 5 | 15 | immutable release manifest | manifest mismatch |
| R-006 | Cost | chosen model is economically unsuitable | 3 | 3 | 9 | model router + cost/request measurement | FinOps budget exceeded |
| R-007 | Reliability | candidate degrades production | 3 | 5 | 15 | Canary + metric gates + stable retained | SLO/eval/security fail |
| R-008 | Governance | numeric targets become “facts” without evidence | 4 | 4 | 16 | COURSE/SOURCE/LAB/PROD labels | undocumented threshold in gate |

## Linkage

R-002 → Security design (14)  
R-003 → Evaluation (13)  
R-005 → CI/CD + MLOps (18–20)  
R-007 → Canary (20)  
R-008 → Metrics & Evidence policy
