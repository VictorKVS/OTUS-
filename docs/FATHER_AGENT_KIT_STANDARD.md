# FATHER Agent Kit Standard

Статус: **CANONICAL DESIGN v1**

## 1. Назначение

Agent Kit — стандартизированный комплект, из которого фабрика собирает логического агента.

Агент не хранит копию общей базы знаний. Он наследует общую базу по versioned reference и добавляет собственные профессиональные пакеты.

~~~text
FATHER BASE AGENT KIT
│
├── Identity / Role Contract
├── K0 FATHER Common Knowledge Core  ← shared reference
├── Common Policies
├── Common Evidence / Traceability
├── Common Lifecycle
├── Common LAB / Evaluation Contract
│
└── ROLE KIT
    ├── K1 Specialist Knowledge Pack(s)
    ├── Skill Pack
    ├── Prompt / Instruction Policy
    ├── Tool / MCP Pack
    ├── Memory Policy
    ├── Workflow Profile
    ├── Security Profile
    ├── Evaluation Profile
    ├── Environment Profile
    └── Agent Dossier
~~~

## 2. Knowledge inheritance

Mandatory formula:

`AGENT KIT = BASE KIT + K0 + K1(s) + optional K2 + Skills + Tools + Policies + Eval`

K0 is a shared reference. K1 is one or more specialist packs. K2 is a project/organization overlay.

Knowledge, Skills, Memory and Experience are separate systems.

## 3. Reuse rule

New agents should be assembled by inheritance/composition, not by copying an existing prompt or knowledge directory.

Reusable assets:
- Common Knowledge Core;
- specialist knowledge packs;
- skill packs;
- tool packs;
- evaluation suites;
- security profiles;
- workflow patterns;
- environment profiles;
- document templates.

## 4. Mandatory Agent Kit fields

- kit_id / version / lifecycle_status;
- agent_id / name / family / role;
- base_kit_id;
- common_core id/version;
- specialist pack ids/versions;
- optional project context;
- skills;
- tools;
- prompts/instruction policy;
- memory scope;
- workflows;
- models/model policy;
- channels;
- permissions/security;
- evaluation profile;
- environment profile;
- dossier path;
- dependencies;
- known limitations.

## 5. Lifecycle

~~~text
KIT DESIGN
→ knowledge compatibility
→ dossier completeness
→ GPT_EMULATED prototype
→ implementation if required
→ FATHER LAB
→ regression / security / multi-LLM
→ VALIDATED
→ CERTIFIED
→ ZOO
→ production use
~~~

## 6. Shared-base change

A K0 change has a large blast radius. It must trigger impact analysis and regression for all dependent agent kits.

K1 changes rerun the affected specialist family.

K2 changes rerun the affected project context tests.

## 7. Status honesty

Allowed statuses:
- DESIGN;
- GPT_EMULATED_READY;
- EXPERIMENTAL;
- CANDIDATE;
- VALIDATED;
- CERTIFIED;
- DEPRECATED;
- QUARANTINED.

A manifest alone never means CERTIFIED.
