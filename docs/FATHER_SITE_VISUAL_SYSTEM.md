# FATHER Site Visual System

Status: **CANONICAL DESIGN v1**

## Goal

FATHER must look like one engineering product, not a collection of unrelated pages.

The visual system is shared by:
- Main FATHER portal;
- Unified System;
- Factory Floor;
- Analytical Core and domain tabs;
- OSINT / Information Security / Pentest / DevSecOps;
- Knowledge Center;
- Agent Kits;
- LAB;
- Trace;
- C00–C99 Dossier;
- current product control screens.

## Visual character

Dark engineering workstation with cyan as the main structural accent.

The visual language must communicate:
- technical control;
- production flow;
- status truth;
- evidence;
- gates;
- traceability;
- controlled progression.

It must **not** look like a marketing dashboard full of decorative KPIs.

## Layout

```text
GLOBAL TOPBAR
│
├─ FATHER
├─ System navigation
└─ current status
        ↓
PAGE HERO / CURRENT CONTEXT
        ↓
PRIMARY WORKSPACE
        ↓
DETAIL / EVIDENCE / CONTROL
        ↓
FOOTER / SYSTEM LINKS
```

## Core colors

- Background: #061019
- Deep background: #030A10
- Panel: #09141C
- Panel secondary: #0C1923
- Lines: #203542
- Text: #E6F1F7
- Muted: #85A0B1
- Cyan: #31C8F4
- Green: #55E69C
- Amber: #FFC857
- Red: #FF7676
- Violet: #B9A2FF

## Status language

Green is reserved for validated/accepted/production truth.

Cyan means active/current/candidate.

Amber means design/experimental/review.

Red means blocked/failed.

Muted means planned/unknown/not active.

## Standard page types

### 1. Main page

Mission + current product + system centers + field tabs + W00-W90 + evidence.

### 2. Domain branch

Common base + K1/K2 overlay + workshop participation + tools + outputs + evidence.

### 3. Workshop

INPUT → REGULATION → ROLE → PROCESS → ARTIFACT → TEST → EVIDENCE → GATE → OUTPUT.

### 4. Control page

One primary action group, explicit result, evidence reference, next permitted action.

## Buttons

Primary action is cyan.

Approval/promotion is green only when the previous automated checks passed.

Danger/blocked controls are red.

Secondary/navigation actions remain dark with structural borders.

## Engineering rule

The visual must never imply a higher maturity than the data model actually has.

**DESIGN must look like DESIGN. EXPERIMENTAL must not look like PRODUCTION.**
