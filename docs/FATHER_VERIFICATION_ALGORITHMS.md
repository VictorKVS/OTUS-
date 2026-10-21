# FATHER Verification Algorithms

Status: DESIGN BASELINE  
Purpose: formal verification algorithms for FATHER LAB, ALINA, OSINT and later specialist lines.

## 1. Result model

Every check returns one of:

- PASS — mandatory criterion satisfied;
- WARN — allowed deviation, requires recorded rationale;
- FAIL — criterion not satisfied;
- BLOCKED — verification cannot run because required evidence/dependency is missing.

A BLOCKED check is never converted to PASS.

## 2. Universal verification algorithm

```text
INPUT: candidate C, baseline B, dataset D, metric policy M, environment E

1. Validate contract/version identifiers.
2. Freeze D, M and E.
3. Verify baseline B is reproducible.
4. Execute baseline on D.
5. Execute candidate C on the same D and equivalent conditions.
6. Capture full traces and artifacts.
7. Compute deterministic metrics.
8. Compute calibrated evaluator metrics.
9. Perform human sample review when policy requires it.
10. Compare C vs B by mandatory floors and deltas.
11. Run regression suite.
12. Run safety/security suite.
13. Run performance/resource/cost suite.
14. Check statistical/repeatability requirements.
15. Build evidence pack.
16. Decide:
    - promote to CANDIDATE/CERTIFIED;
    - keep as EXPERIMENTAL;
    - reject;
    - quarantine.
OUTPUT: decision + evidence + reproducible run manifest.
```

## 3. A/B/N comparison algorithm

Requirements:

- same task set;
- same dataset version;
- same scoring rubric;
- same environment class;
- equivalent tool/data access;
- randomized/counterbalanced ordering when order can bias results;
- repeated runs for stochastic configurations.

Compare:

- absolute metric floors;
- paired delta vs baseline;
- variance;
- confidence interval;
- failure categories;
- cost/latency/resource trade-offs.

Default statistical rule: use paired comparison when the same cases are evaluated across variants. Report effect size and 95% confidence interval; project policy may override the confidence level. Do not promote merely because an average score is numerically higher.

## 4. Prompt verification

For prompt Pn:

1. Freeze model and all non-prompt settings.
2. Run baseline prompt P0 on dataset D.
3. Run Pn on D.
4. Score:
   - task success;
   - factual correctness;
   - completeness;
   - instruction following;
   - source/evidence fidelity;
   - hallucination rate;
   - format validity;
   - safety;
   - tokens;
   - latency;
   - cost;
   - stability across repeats.
5. Inspect failure clusters.
6. Run protected regression cases.
7. Promote only if mandatory quality/safety floors hold.

Prompt changes that improve style but reduce correctness/evidence cannot become Champion for quality-critical profiles.

## 5. RAG verification

Evaluate retrieval and generation separately.

### Retrieval metrics
- Recall@K;
- Precision@K;
- MRR;
- NDCG where ranking relevance is graded;
- evidence coverage;
- context relevance;
- duplicate/noise ratio.

### Generation metrics
- answer correctness;
- faithfulness to retrieved evidence;
- citation correctness;
- completeness;
- unsupported-claim rate;
- abstention correctness.

Algorithm:

```text
QUERY
→ expected evidence set
→ retriever
→ compare retrieved vs expected
→ reranker
→ context builder
→ generator
→ compare answer vs gold/evidence
→ trace attribution to retrieved chunks
```

A generation score cannot hide poor retrieval. Both layers keep separate metrics.

## 6. Knowledge algorithm verification

For fact/entity/relation/provenance/graph algorithms:

1. Use human-verified document fragments.
2. Freeze ontology/schema.
3. Run candidate extraction.
4. Compare against gold labels.
5. Compute:
   - precision;
   - recall;
   - F1;
   - duplicates;
   - missed entities/relations;
   - wrong entity merges;
   - wrong relation direction/type;
   - provenance accuracy;
   - version/date attribution accuracy;
   - contradiction detection precision/recall.
6. Rebuild graph in isolated namespace.
7. Execute graph consistency checks.
8. Run downstream retrieval/query tests.
9. Reject if graph quality improves locally but damages downstream answers.

## 7. Agent verification

The final answer is not sufficient.

Evaluate:

- task success;
- plan quality;
- steps count;
- unnecessary loops;
- tool selection;
- tool arguments;
- retrieval quality;
- handoff correctness;
- permissions;
- recovery after tool/model failure;
- timeouts/retries;
- human approval compliance;
- cost;
- latency;
- safety;
- final evidence.

Trajectory algorithm:

```text
TASK
→ PLAN
→ ACTION
→ OBSERVATION
→ NEXT ACTION ...
→ RESULT

for every step:
  validate permitted action
  validate tool choice
  validate arguments/schema
  validate state transition
  validate evidence linkage
  detect loops/repeats
  record cost/latency/errors
```

## 8. Skill verification

A skill is not “learned” because one example succeeded.

Check:

- theory/knowledge prerequisites;
- controlled exercises;
- unseen cases;
- transfer to adjacent cases;
- retention after time/version change;
- regression after other skills/models are changed;
- evidence of successful real tasks.

Specialist level promotion requires a policy-defined combination of test, practice, real result and retained evidence.

## 9. Evaluator verification

Evaluator calibration:

1. Build expert-labeled calibration set.
2. Run evaluator on the same set.
3. Measure:
   - agreement;
   - confusion matrix for categorical decisions;
   - correlation for ordinal/numeric scores;
   - systematic bias by category;
   - variance across repeats;
   - sensitivity to prompt/order.
4. Reject or restrict evaluator if calibration is insufficient.
5. Version evaluator and rubric together.

Changing evaluator version invalidates direct comparison unless a bridge calibration is performed.

## 10. Tool/MCP verification

For every tool:

- schema validation;
- permission boundary;
- authentication/secrets handling;
- expected success case;
- bad input;
- timeout;
- dependency unavailable;
- partial response;
- malformed response;
- retry/idempotency;
- audit trail;
- safe failure.

Tools with side effects require explicit approval policy and rollback/compensation design.

## 11. Workflow verification

Check:

- every node has a contract;
- inputs/outputs match;
- retries are bounded;
- idempotent steps are marked;
- non-idempotent steps have compensation/approval;
- parallel branches merge deterministically;
- dead ends are detectable;
- loops have termination conditions;
- failure routes exist;
- human-in-loop gates cannot be bypassed.

## 12. DevOps environment verification

For each environment profile:

### Reproducibility
- creation from versioned code/config;
- no undocumented manual step required;
- image/artifact versions pinned.

### Isolation
- namespace/project/tenant boundary;
- network policy;
- service account/RBAC;
- secrets boundary;
- resource quota/limits.

### Observability
- logs;
- metrics;
- traces;
- correlation id;
- health/readiness;
- experiment/run id linkage.

### Rollback / recovery
- deployment rollback tested;
- state backup/restore tested where stateful;
- failure drill evidence retained.

### Security
- dependency/container/IaC/secret scanning;
- least privilege;
- signed/traceable artifacts where required.

### Resource control
- CPU/RAM/GPU/storage limits;
- timeout/concurrency limits;
- cost visibility.

Environment status cannot become READY when a mandatory gate is FAIL/BLOCKED.

## 13. Safety / adversarial verification

This section is defensive validation only.

Check resilience against:

- prompt injection;
- poisoned/untrusted retrieved content;
- secret/data leakage;
- excessive agency;
- unsafe tool invocation;
- permission bypass attempts;
- malformed/oversized input;
- misleading tool output;
- model/tool unavailability;
- corrupted state.

Run only in approved test environments. Potentially dangerous scenarios require isolated/disposable infrastructure and must not target external systems without authorization.

## 14. Regression algorithm

```text
candidate passes target test
→ load protected regression suite
→ execute all previously fixed failures
→ execute critical capability tests
→ compare against previous champion
→ classify regressions
→ BLOCK promotion if mandatory capability regresses
```

Every production defect that is reproducible should become a regression case after review.

## 15. Promotion algorithm

```text
if required_evidence_missing:
    BLOCKED
elif mandatory_quality_floor_failed:
    FAIL
elif safety_gate_failed:
    FAIL
elif critical_regression_detected:
    FAIL
elif environment_gate_failed:
    BLOCKED/FAIL
else:
    evaluate profile objective
    if challenger materially improves target profile
       and non-target metrics remain inside allowed floors:
          CANDIDATE → CERTIFIED
    else:
          KEEP CHAMPION
```

Production promotion may additionally require human approval.

## 16. Production feedback algorithm

```text
PRODUCTION TRACE / USER FEEDBACK / INCIDENT
→ normalize event
→ classify: bug / quality / safety / cost / latency / unknown
→ reproduce
→ create case
→ human review
→ add to proper dataset
→ create hypothesis
→ run experiment
→ regression
→ promote or reject
```

This closes the factory learning loop without allowing uncontrolled self-modification.
