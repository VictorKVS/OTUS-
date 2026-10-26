# FATHER · Evidence, Ownership, Contracts and Innovation Review

Status: **CANONICAL DESIGN v1**

## 1. Two separate questions

FATHER must never merge these claims:

1. **Ownership / provenance evidence** — who created or modified an artifact, using which inputs, agents, models, tools, versions and sources.
2. **Innovation / novelty review** — what architectural, contractual or functional difference exists relative to known analogues.

A strong provenance chain does **not** prove novelty.
A novelty hypothesis does **not** prove legal ownership or patentability.

## 2. Embedded contracts

Every FATHER block has versioned contracts:

- Input/Output;
- Role/Authority;
- Data/Knowledge;
- Runtime/Tool;
- Evidence;
- Ownership/Provenance.

Every edge in the project graph must resolve to a compatible producer/consumer contract.

## 3. Ownership evidence bundle

```text
REQUIREMENT / IDEA
  ↓
ARCHITECTURE / ADR
  ↓
HUMAN + AGENT CONTRIBUTION
  ↓
PROMPT / MODEL / TOOL VERSION
  ↓
CODE / DATA / CONFIG
  ↓
COMMIT / HASH / BUILD
  ↓
TEST / LAB EVIDENCE
  ↓
RELEASE
```

Recommended controlled artifacts:

- `PROVENANCE.json`
- `OWNERSHIP.md`
- `SIGNATURE.txt`
- `CHECKSUMS.sha256`
- `SBOM.json`
- `EVIDENCE/`
- Contract manifests
- Source/license registry

## 4. Analogue and robot-decomposition review

For professional projects, FATHER should search known comparable robots/systems and decompose them using the **same taxonomy** as our design.

```text
OUR PRODUCT
  ↓ common taxonomy
BLOCKS / FUNCTIONS / CONTRACTS / METRICS

KNOWN ROBOT A
  ↓ same taxonomy
BLOCKS / FUNCTIONS / CONTRACTS / METRICS

KNOWN ROBOT B
  ↓ same taxonomy
BLOCKS / FUNCTIONS / CONTRACTS / METRICS

              ↓ ALIGN / COMPARE

COMMON
REUSED
ADAPTED
DIFFERENT
NOVELTY HYPOTHESIS
```

Comparison must include more than visible components. It must compare:

- functional decomposition;
- interfaces/contracts;
- orchestration;
- data/knowledge flow;
- safety;
- failure modes;
- tests;
- metrics;
- update/learning loop.

## 5. Pro Mode

For `PRO_MODE`, commercial release, ownership claims or invention candidates, Gate `G-PRO-IP-PROVENANCE` is mandatory.

Pass requires:
- full provenance;
- license/rights review;
- versioned contracts;
- analogue search log;
- decomposition comparison;
- scoped novelty claims;
- independent verification.

Unresolved originality is `NOVELTY_HYPOTHESIS`, never `PROVEN_INVENTION`.
