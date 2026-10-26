# FATHER Avatar Operator Architecture

Status: **CANONICAL DESIGN v1**

## Core rule

**Avatar is not the LLM.**

User sees one FATHER avatar, but internally the system is decomposed into replaceable layers:

```text
USER
  ↓
AVATAR SHELL
(static now → interactive video later)
  ↓
FATHER OPERATOR AGENT
(role / dialogue policy / routing)
  ↓
KNOWLEDGE / RAG
  ↓
MODEL ROUTER
  ↓
LLM
  ↓
PROMPT / RUN
  ↓
VOICE / TTS
  ↓
AVATAR SHELL
  ↓
USER
```

## FTH-AV-001

Canonical avatar identity: **FATHER Operator**.

The visible avatar is only the human-facing shell.  
The production assistant role is `FTH-AG-OPR-001`.

## MVP

First implementation:

- static avatar;
- text chat;
- microphone trigger;
- state machine: IDLE / LISTENING / THINKING / RESPONDING / HANDOFF / BLOCKED;
- FATHER Operator role;
- project context;
- K0 + routed K1/K2 knowledge;
- Model Router;
- existing TTS component.

## Upgrade path

```text
STATIC IMAGE
→ SIMPLE ANIMATION
→ LIPSYNC
→ INTERACTIVE VIDEO AVATAR
```

No upgrade may change the operator/knowledge/model contracts unnecessarily.

## Routing

FATHER Operator answers simple factory-navigation questions itself.

Specialist work is handed off:

- analytics → ALINA;
- architecture → FATHER Architect;
- code → FATHER Programmer / CODEX;
- OSINT → OSINT Lead;
- quality/evaluation → QA/LAB;
- security → Security Engineer;
- deployment → DevOps/SRE.

## Metrics

- intent classification accuracy;
- routing accuracy;
- grounded answer rate;
- handoff correctness;
- response latency;
- user correction rate;
- voice playback success;
- UI state transition correctness.

## Evidence

Every response can carry:

- operator agent id;
- operator prompt version/hash;
- model id/version;
- knowledge references;
- routing trace;
- run id;
- TTS trace id where applicable.

This allows the avatar to remain one visible persona while the internal factory stays modular, testable and replaceable.
