# FATHER Shared Knowledge Reuse Matrix

Статус: **CANONICAL DESIGN v1**

## Principle

Общая база знаний не размножается по агентам. Все комплекты используют `KB-K0-FATHER-COMMON` как `shared_reference`.

~~~text
                         K0 FATHER COMMON
                                │
      ┌─────────────┬───────────┼───────────┬──────────────┐
      ▼             ▼           ▼           ▼              ▼
   ALINA        ARCHITECT     CODEX      KNOWLEDGE       QUALITY
      │             │           │           │              │
 K1 Analytics  K1 Architect K1 Programmer K1 KnowEng  K1 Quality
      │
      └──────────────→ OSINT also inherits Analytics + OSINT K1

SECURITY = K0 + IB K1 + DevSecOps K1
SRE      = K0 + DevSecOps K1 + Ops/SRE K1
FACTORY  = K0 + Factory Orchestration K1
~~~

## Sharing model

When a new agent is created:
1. attach compatible K0 version;
2. attach one or more K1 packs;
3. optionally attach K2 project context;
4. attach role Skills/Tools/Policies;
5. create independent memory scope;
6. validate kit;
7. run LAB before certification.

K0 update triggers regression across all dependent kits. K1 update affects its dependent families. K2 affects only project-scoped agents.