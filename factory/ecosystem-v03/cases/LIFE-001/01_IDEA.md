# LIFE-001 · IDEA

**Status:** IDEA_DRAFT  
**Stage:** 01 — IDEA  
**Project:** Personal Lifelong Companion / Human Life Agent  
**Important:** this document captures the product idea only. It is not yet a Product Brief, security design, business analysis, system analysis, architecture, or implementation specification.

---

# 1. One-sentence idea

Create a personal digital companion that can accompany one person throughout life, preserve continuity of context, help organize information and decisions, and adapt its capabilities to the person's current life stage.

---

# 2. Core problem hypothesis

A person's important information, decisions, documents, goals, history, knowledge, health context, education, work, finances, household matters, relationships with institutions, and personal preferences are fragmented across people, applications, documents, organizations, and time.

As life changes, context is repeatedly lost.

The product hypothesis is that one continuously evolving personal system can preserve useful context across decades and help the person understand:

- what has happened;
- what matters now;
- what needs attention;
- what options exist;
- what was decided before and why;
- what documents/evidence support a decision;
- what should be handed to another person or specialist.

---

# 3. Primary value proposition

Not "an AI that lives instead of the person."

The intended value is:

```text
CONTINUITY OF PERSONAL CONTEXT
        +
ORGANIZATION OF LIFE INFORMATION
        +
ASSISTANCE WITH DECISIONS AND TASKS
        +
MEMORY / EVIDENCE / HISTORY
        +
ADAPTATION TO LIFE STAGE
```

The human remains the principal subject and decision owner.

---

# 4. Life-stage hypothesis

The same product may change its role over time.

```text
BIRTH / EARLY CHILDHOOD
        ↓
CHILDHOOD
        ↓
EDUCATION
        ↓
ADOLESCENCE
        ↓
EARLY ADULTHOOD
        ↓
CAREER / FAMILY / HOUSEHOLD
        ↓
MATURE ADULTHOOD
        ↓
RETIREMENT
        ↓
LATE-LIFE SUPPORT
        ↓
END-OF-LIFE / DIGITAL LEGACY HANDOFF
```

This does NOT imply one monolithic agent. It is a lifecycle product concept whose internal modules may change by age, authority, law, need, and context.

---

# 5. Candidate life domains

These are idea-level domains only and are not approved scope.

- identity and personal documents;
- family and household;
- education and learning;
- health and wellness context;
- career and professional development;
- finances and property;
- legal and administrative matters;
- travel and mobility;
- goals, plans, habits, reminders;
- personal knowledge and memory;
- digital assets and accounts;
- communications and important contacts;
- purchases, subscriptions, warranties, services;
- safety and emergency information;
- care of dependents;
- retirement and long-term planning;
- end-of-life instructions and digital legacy.

---

# 6. Conceptual inputs

At idea level, the system may eventually receive information from:

- the person;
- parents/guardians when legally appropriate;
- documents and files;
- connected services;
- calendars/messages/approved communications;
- health or activity systems where permitted;
- public information;
- professional specialists;
- household devices/sensors;
- historical records created by the system itself.

No source is assumed trusted merely because it is connected.

---

# 7. Conceptual outputs

The product may eventually produce:

- reminders and next actions;
- structured personal timeline;
- explanations and summaries;
- decision options;
- checklists;
- prepared documents/drafts;
- questions for doctors, lawyers, teachers, employers, banks, government services, etc.;
- warnings about conflicts, deadlines, missing information, or risks;
- personal knowledge views;
- history of important decisions;
- evidence/provenance references;
- handoff packages for a human specialist;
- emergency or continuity packages where explicitly configured.

---

# 8. Human authority principle

The initial idea assumes:

```text
AGENT ASSISTS
HUMAN DECIDES
```

Any future autonomous action must be separately justified, authorized, bounded, and reviewed.

This is especially important for health, finance, legal matters, children, safety-critical actions, and irreversible operations.

---

# 9. Continuity principle

The key differentiator is not a chatbot interface.

The differentiator is continuity:

```text
EVENT
  ↓
PERSONAL CONTEXT
  ↓
DECISION
  ↓
ACTION
  ↓
RESULT
  ↓
EVIDENCE / HISTORY
  ↓
FUTURE CONTEXT
```

The system should be able to explain what it knows, where it came from, what changed, and what remains uncertain.

---

# 10. Ownership / control hypothesis

The long-term design should aim for the person to remain the primary owner/controller of their personal context.

For minors or persons who cannot exercise full control, authority and delegation must be explicitly modeled rather than assumed.

Transition of authority across life stages is therefore a core product problem, not an implementation detail.

---

# 11. What this idea is NOT

At this stage the product is NOT defined as:

- a medical diagnosis system;
- an autonomous financial adviser;
- an autonomous legal representative;
- a surveillance system;
- a social scoring system;
- a substitute parent/guardian;
- a system that makes irreversible life decisions for the person;
- a single LLM with permanent unrestricted access to all personal data;
- a mandatory cloud service;
- a finished architecture.

---

# 12. Key assumptions to challenge later

A-001. People will value long-term continuity enough to maintain such a system.  
A-002. Trust can be earned over decades.  
A-003. Data ownership/portability can survive vendor and technology changes.  
A-004. The product can adapt to changing law, family status, age, capacity, and jurisdiction.  
A-005. Sensitive domains can be isolated rather than pooled into one unrestricted memory.  
A-006. A useful continuity layer can exist without becoming invasive surveillance.  
A-007. The system can explain uncertainty and provenance sufficiently for high-stakes use.  
A-008. Authority can transition safely from guardian-controlled to person-controlled operation.  
A-009. The system can degrade gracefully when integrations, models, or providers disappear.  
A-010. A person's history can be preserved without freezing outdated beliefs or wrong data forever.

---

# 13. Open questions for the next stage

These are questions for Product Manager discovery, not answers:

1. Who is the first real paying/using customer?
2. Is this one product, a platform, or a family of life-stage products?
3. What is the first narrow problem worth solving?
4. When should the lifecycle actually begin: birth, first device, first document, first account?
5. Who controls the system for a child?
6. How and when is control transferred to the person?
7. What information must never be centralized?
8. Which life domains are mandatory for MVP and which are excluded?
9. What happens when two trusted humans disagree?
10. What is the smallest useful version that proves continuity value?
11. What data remains local-only?
12. What should survive model/provider replacement?
13. What is the offboarding/export/deletion story?
14. What does "success after 10 years" mean?
15. What happens at death or incapacity?
16. Who is allowed to receive legacy information?
17. Which decisions must always remain human?
18. How does the product handle incorrect historical data?
19. How does it distinguish fact, interpretation, recommendation, and preference?
20. What evidence must accompany a recommendation?

---

# 14. Initial success hypothesis

The product is valuable if, over time, it helps the person lose less context and make better-organized decisions without taking away human control.

Candidate long-term measures:

- fewer missed obligations/deadlines;
- faster preparation for important decisions;
- lower duplication of documents and repeated explanations;
- higher traceability of important decisions;
- lower time to assemble information for a specialist;
- successful migration across devices/providers;
- low rate of harmful or unauthorized actions;
- user trust and continued voluntary use.

These measures are hypotheses and must be refined by Product Manager.

---

# 15. Handoff

```text
IDEA_DRAFT
    ↓
PRODUCT MANAGER DISCOVERY
    ↓
PRODUCT BRIEF
    ↓
INFORMATION SECURITY INTAKE
    ↓
BUSINESS ANALYSIS
    ↓
SYSTEM ANALYSIS
    ↓
ARCHITECTURE
```

The next stage must not design implementation. It must test and narrow the product hypothesis.
