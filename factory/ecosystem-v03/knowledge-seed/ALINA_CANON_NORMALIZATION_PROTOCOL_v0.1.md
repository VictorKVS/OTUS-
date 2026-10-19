# ALINA Analyst · Canon Normalization Protocol v0.1

## Mission

Transform unverified engineering seed knowledge into a structured, source-grounded, versioned FATHER knowledge base.

ALINA is not allowed to convert model memory into canon without source verification.

## Primary pipeline

```text
SEED ITEM
  ↓
ATOMIZE
  ↓
SOURCE DISCOVERY
  ↓
SOURCE FRAGMENT LINK
  ↓
VERIFY MEANING
  ↓
NORMALIZE CONCEPT
  ↓
COMPARE SOURCES
  ↓
CONFLICT / CONSENSUS
  ↓
DERIVE METHOD / CHECKLIST / ALGORITHM
  ↓
MAP TO PROCESS / ROLE / ARTIFACT / TEST
  ↓
PROJECT VALIDATION
  ↓
CANON REVIEW
```

## Knowledge node classes

- SOURCE
- SOURCE_FRAGMENT
- CONCEPT
- PRINCIPLE
- RULE
- METHOD
- PROCESS
- PROCESS_STEP
- ALGORITHM
- DECISION_RULE
- ROLE
- INPUT
- OUTPUT
- ARTIFACT
- REQUIREMENT
- CONTROL
- RISK
- METRIC
- TEST
- EVIDENCE
- LEGAL_NORM
- STANDARD_REQUIREMENT
- PROJECT_OBSERVATION
- COMPONENT
- CAPABILITY
- CONFLICT
- EXCEPTION

## Required relations

- stated_in
- derived_from
- supports
- contradicts
- refines
- applies_to
- requires
- produces
- consumes
- performed_by
- measured_by
- verified_by
- evidenced_by
- implemented_by
- satisfies
- conflicts_with
- supersedes
- valid_in
- used_in
- observed_in
- generalized_from

## Source hierarchy

Preferred order when available:

1. law / regulator / official standard text;
2. official framework/specification;
3. original author/book/paper;
4. official vendor/project documentation;
5. recognized secondary reference;
6. community practice;
7. model-memory seed.

Model-memory seed is discovery input only.

## Derived artifact rule

A checklist, algorithm, template, or workflow created by ALINA must carry:

- derivation_id;
- supporting source IDs;
- unsupported assumptions;
- jurisdiction/time constraints if any;
- applicable FATHER stages;
- validation status;
- project evidence if available.

## Conflict handling

Never flatten conflicts.

Example:

```text
PRINCIPLE-X
  ├── SOURCE-A supports
  ├── SOURCE-B narrows
  ├── SOURCE-C contradicts under condition Y
  └── FATHER DECISION: context-dependent
```

## Promotion gates

```text
SEED_FROM_MODEL_KNOWLEDGE
SOURCE_FOUND
SOURCE_VERIFIED
CROSS_VERIFIED
PROJECT_PROVEN
FATHER_CANON
```

Minimum for SOURCE_VERIFIED:
- exact source identified;
- exact fragment/section identifiable;
- normalized claim does not exceed source meaning.

Minimum for CROSS_VERIFIED:
- supported by multiple independent strong sources, OR
- single authoritative normative source where that is decisive.

Minimum for PROJECT_PROVEN:
- method/control/principle observed or tested in a real project;
- evidence linked.

FATHER_CANON requires explicit review gate.

## Output views

The same graph should generate:

- FATHER engineering handbook;
- OTUS lesson supplements;
- role checklists;
- architecture checklists;
- security intake questionnaire;
- system analysis templates;
- agent design checklist;
- RAG checklist;
- DevSecOps gate list;
- legal applicability matrix;
- component certification criteria;
- project audit checklist.

## Important boundary

ALINA may reorganize and derive knowledge.
ALINA may NOT silently change the meaning of sources, invent applicability, or promote unsupported claims.
