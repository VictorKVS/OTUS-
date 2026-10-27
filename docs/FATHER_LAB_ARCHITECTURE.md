# FATHER Research & Test Center — Architecture Standard

Status: DESIGN BASELINE  
Scope: FATHER / ALINA / OSINT / future specialist lines  
Rule: evidence before promotion.

## 1. Purpose

FATHER LAB is the common experimentation, metrology, validation and certification layer of the factory.

It is not a standalone playground. Every project receives a project-specific view over the same Experimentation Engine.

```text
PROJECT
→ BASELINE
→ HYPOTHESIS
→ CONTROLLED VARIANT
→ A/B/N RUN
→ EVALUATION
→ HUMAN SAMPLE REVIEW
→ REGRESSION
→ SAFETY
→ PERFORMANCE / COST
→ CERTIFICATION
→ CHAMPION
→ PRODUCTION
→ REAL-WORLD FEEDBACK
→ NEXT EXPERIMENT
```

## 2. Mandatory laboratory domains

- Model Lab — LLM/VLM/embedding/reranker comparison.
- Prompt Lab — prompt/system-prompt versioning and A/B/N.
- RAG Lab — chunking, embeddings, retrieval, reranking, context building.
- Knowledge Algorithm Lab — facts, entities, relations, provenance, contradictions, graph construction.
- Agent Lab — task success, trajectory, tool use, handoffs, recovery.
- Skill Lab — skill acquisition, transfer, retention and regression.
- Memory Lab — scope, retrieval, contamination, forgetting and isolation.
- Workflow Lab — routing, parallelism, retries, idempotency and human approval.
- Tool/MCP Lab — correctness, permissions, timeouts, failure handling.
- Evaluator Lab — judge/scorer calibration and measurement error.
- Safety / Red Team Lab — defensive adversarial validation of the AI system.
- Performance Lab — latency, throughput, concurrency and resources.
- Cost Lab — cost/run, cost/success, GPU/token/storage/egress.
- Benchmark Center — version-to-version benchmark suites.
- Dataset Center — versioned reference datasets.
- Certification Center — final promotion decision and evidence pack.

## 3. One engine, many project labs

```text
                 FATHER EXPERIMENTATION ENGINE
                            │
          ┌─────────────────┼─────────────────┐
          ▼                 ▼                 ▼
      FATHER LAB         ALINA LAB         OSINT LAB
          │                 │                 │
          └─────────────────┼─────────────────┘
                            ▼
                 datasets / runs / metrics
                 traces / evaluators / gates
                 champions / evidence
```

Future IB, Pentest, DevSecOps, Legal, Programmer and other labs must reuse the same engine.

## 4. ALINA Research Center

ALINA uses the common engine but has its own research views:

- Prompt Lab;
- RAG Lab;
- Knowledge Algorithm Lab;
- Agent Lab;
- Skill Lab;
- Evaluator Lab;
- Memory Lab;
- Optimization Lab;
- Training Lab.

ALINA may propose a hypothesis or challenger automatically, but cannot promote it to production by itself unless the configured human-approval policy permits that class of change.

## 5. Experiment contract

Every experiment must record:

- experiment_id;
- project_id;
- hypothesis;
- baseline configuration;
- challenger configuration(s);
- dataset id + immutable version;
- code/git revision;
- model/provider/version;
- prompt version;
- RAG/retrieval configuration;
- agent/workflow configuration;
- tool versions;
- evaluator versions;
- environment;
- deterministic settings/seed where supported;
- start/end timestamps;
- traces;
- raw outputs;
- metrics;
- cost/resources;
- errors;
- decision;
- evidence artifacts.

A result without this passport is exploratory only and cannot be used for promotion.

## 6. Dataset classes

```text
TRAIN
DEV
VALIDATION
TEST
GOLDEN
BENCHMARK
REGRESSION
ADVERSARIAL
EDGE CASES
PRODUCTION FAILURES
HUMAN VERIFIED
SYNTHETIC
```

Golden/regression/adversarial sets are versioned and protected from accidental training contamination.

Production failures are reviewed before entering regression datasets.

## 7. Metrology

FATHER must measure the measurement system itself.

Evaluator/Judge records:

- evaluator id/version;
- rubric;
- human-gold calibration set;
- agreement with expert labels;
- false-positive/false-negative rates where applicable;
- variance/repeatability;
- cost/latency;
- known limitations.

LLM-as-judge is never treated as ground truth without calibration.

## 8. Champion / Challenger

There is no single universal “best model”.

Champion is selected per operating profile:

- QUALITY;
- BALANCED;
- FAST;
- CHEAP;
- LOCAL;
- SECURE / OFFLINE;
- HIGH-THROUGHPUT;
- project-specific profiles.

A challenger may replace a champion only when all mandatory gates pass.

## 9. Promotion states

```text
IDEA
→ RESEARCH
→ PROTOTYPE
→ EXPERIMENTAL
→ CANDIDATE
→ VALIDATED
→ CERTIFIED
→ CHAMPION / PRODUCTION
```

Additional terminal/control states:

- REJECTED;
- FAILED;
- QUARANTINED;
- DEPRECATED;
- SUPERSEDED.

## 10. Factory rule

No Model, Prompt, RAG configuration, Knowledge algorithm, Agent, Skill, Tool, Workflow, Evaluator or Guardrail becomes a standard FATHER component without:

1. reproducible run;
2. versioned dataset;
3. frozen evaluator/metric set;
4. comparison with baseline;
5. regression suite;
6. safety checks;
7. retained evidence;
8. promotion decision.

This rule applies to FATHER itself.
