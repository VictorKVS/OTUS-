# FATHER Workshop Standard

Status: **CANONICAL DESIGN v1**

Every production workshop W00–W90 implements the same control contract:

```text
INPUT
→ REGULATIONS
→ OWNER / RESPONSIBLE ROLE
→ PROCESS
→ ARTIFACTS
→ TESTS / VALIDATION
→ EVIDENCE
→ GATE
→ OUTPUT
→ NEXT WORKSHOP
```

The canonical workshop registry is machine-readable at:

`factory/data/workshop-registry.json`

## Rules

- No workshop may silently skip its required regulation.
- Generated artifacts are not accepted until their required tests pass.
- Evidence must identify versions, sources, test/run IDs or equivalent provenance.
- A Gate is a promotion decision, not a decorative status.
- Critical verification roles must remain independent from the author of implementation.
- Product tailoring may mark specific artifacts/tests N/A only with explicit rationale and evidence.

## Workshops

### W00 · INTAKE

**Owners:** Product Owner, ALINA Analyst

**Gate:** G-W00-INTAKE

**Output:** accepted work package; initial scope; project id; opened controlled dossier

### W10 · ANALYSIS

**Owners:** ALINA Analyst

**Gate:** G-W10-ANALYSIS

**Output:** validated analytical bundle

### W20 · ARCHITECTURE

**Owners:** FATHER Architect

**Gate:** G-W20-ARCH

**Output:** approved architecture package; validated Development Pack

### W30 · KNOWLEDGE_DATA

**Owners:** Knowledge Engineer, Data Engineer

**Gate:** G-W30-KNOWLEDGE-DATA

**Output:** approved knowledge/data package

### W40 · AGENT_COMPONENT_ENGINEERING

**Owners:** FATHER Architect, Factory Controller

**Gate:** G-W40-COMPONENTS

**Output:** approved implementation bill and agent/component plan

### W50 · IMPLEMENTATION

**Owners:** FATHER Programmer / CODEX

**Gate:** G-W50-IMPLEMENTATION

**Output:** implementation candidate

### W60 · QA_SECURITY_LAB

**Owners:** QA/Evaluator, Security Engineer, Pentest role where authorized

**Gate:** G-W60-QUALITY-SECURITY

**Output:** verified candidate or blocked findings

### W70 · DEVOPS_ENVIRONMENTS

**Owners:** DevOps/SRE

**Gate:** G-W70-OPERATIONS

**Output:** operational release candidate

### W80 · ACCEPTANCE_CERTIFICATION

**Owners:** Certifier, Product Owner, Independent reviewers

**Gate:** G-W80-ACCEPTANCE

**Output:** approved release or blocked candidate

### W90 · OUTPUT_DELIVERY

**Owners:** Factory Controller, Product Owner, Operations

**Gate:** G-W90-DELIVERY

**Output:** verified delivered product; experience/feedback stream

