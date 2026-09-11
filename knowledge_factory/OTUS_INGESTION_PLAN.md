# OTUS Knowledge Ingestion Conveyor

**Status:** ACTIVE DESIGN / MVP  
**Goal:** use the same FATHER Knowledge Factory principles for OTUS study materials without mixing them with LEGAL lifecycle semantics.

## 1. Scope

OTUS corpus has three source classes:

1. `LOCAL_OTUS` — files already present in this repository: PDFs, TXT notes, notebooks, code, diagrams.
2. `PUBLIC_REFERENCE` — public primary/authoritative references used by lessons: official documentation, standards, project docs, public papers and source repositories.
3. `ACCESS_CONTROLLED` — course pages/materials available only through an authenticated OTUS account or other restricted access. These may be processed locally when lawfully available to the user, but must not be mirrored automatically into the public repository.

The knowledge pipeline is:

```text
LESSON / HOMEWORK
  -> MATERIAL REGISTRY
  -> SOURCE / RIGHTS / TRUST CHECK
  -> ORIGINAL OR REPOSITORY SNAPSHOT
  -> SHA-256 + MIME + VERSION/SNAPSHOT
  -> STRUCTURE
  -> CHUNKS
  -> TERMS / CONCEPTS / PATTERNS / ALGORITHMS / CHECKLISTS
  -> DIAGRAM/FIGURE REFERENCES
  -> LESSON LINKS
  -> OTUS_KB REVIEW PACKAGE
```

## 2. Do not duplicate the Knowledge Factory engine

The processing engine belongs to `OSINT_deepseek` / FATHER Knowledge Factory. OTUS stores only:

- lesson/source registry;
- local course artifacts already owned by this repository;
- sanitized review manifests;
- lesson-to-knowledge mappings;
- derived summaries/checklists/diagrams that are lawful to publish.

This is the second-profile reuse proof for the Knowledge Factory: the same provenance/structure/chunk machinery must work for `WEB`, `BOOK`, `SCIENCE`, `STANDARD`, `VENDOR_DOC` and local course material without legal lifecycle fields.

## 3. Stable object chain

```text
OTUSCourse
 -> Lesson
 -> MaterialSource
 -> MaterialSnapshot
 -> StructureNode
 -> Chunk
 -> Concept
 -> Pattern
 -> Algorithm
 -> Checklist
 -> DiagramRef
 -> Example
 -> Relation
 -> ReviewDecision
 -> OTUSKnowledgeObject
```

Minimum IDs:

```text
OTUS-L{lesson:02d}
OTUS-L{lesson:02d}-SRC-{slug}
OTUS-L{lesson:02d}-MAT-{slug}
OTUS-L{lesson:02d}-CH-{stable-hash}
OTUS-L{lesson:02d}-KO-{stable-id}
```

## 4. Decomposition rules

### Local TXT/Markdown

Preserve file SHA and path, then split by headings, lists, paragraphs, code fences and explicit task/checklist sections.

### HTML documentation

Preserve requested URL, final URL, timestamp and SHA of fetched bytes. Split by semantic headings (`h1..h6`), paragraphs, lists, tables and code blocks. Keep image/diagram URLs as references; do not silently copy third-party images unless license permits redistribution.

### PDF

Preserve exact PDF bytes and page count. Structure nodes must retain page locators. Extracted text is a derivative, never a replacement for the PDF. Figures/tables are referenced by page and caption where available.

### Git repository

Prefer immutable commit SHA/tag over a moving branch when a snapshot is used for evidence. Capture repository URL, commit SHA, license, selected paths and hashes. Do not copy entire unrelated repositories into OTUS when only a bounded documentation/source subset is needed.

### Notebook/code

Split notebook into markdown/code/output cells with stable cell order. Code examples retain source path and commit/blob identity. Do not promote code output to general architectural knowledge without review.

## 5. Knowledge extraction profile

For OTUS, preliminary analysis should identify separately:

- `TERM` / glossary candidate;
- `CONCEPT`;
- `ARCHITECTURE_PATTERN`;
- `ANTI_PATTERN`;
- `ALGORITHM` / ordered procedure;
- `CHECKLIST_ITEM`;
- `DECISION_CRITERION`;
- `TRADEOFF`;
- `METRIC`;
- `FORMULA`;
- `EXAMPLE`;
- `DIAGRAM_REF`;
- `TOOL` / technology;
- `RISK`;
- `ASSUMPTION`;
- `HOMEWORK_REQUIREMENT`.

No automatic cast from tutorial example to universal best practice. Every derived object retains lesson/source provenance.

## 6. Initial public-reference seed

The first registry covers already discussed high-value sources:

- Lesson 6 — C4 model official site and diagram hierarchy;
- Lesson 7 — LangChain learn/retrieval/RAG/knowledge-base documentation;
- Lesson 9 — MADR documentation and source repository;
- Lesson 15 — OWASP GenAI LLM Top 10 and Grafana documentation;
- Lesson 18 — HashiCorp Terraform official tutorials;
- Lesson 20 — Argo CD architecture;
- Lesson 24 — KEDA scaling concepts;
- Lesson 30 — Hugging Face Model Cards + Model Cards paper.

Known but unresolved sources remain `SOURCE_PENDING` rather than being guessed: Risk Register donor for lesson 3, VRAM calculator for lesson 17, specific OAuth/terraform donor pages, semantic-cache donor, and any access-controlled OTUS pages.

## 7. Review package

For each processed source produce metadata suitable for GitHub review:

```text
lesson_id
material_id
source_class
source_url / repository path
snapshot/commit/version
sha256
mime/type
license/rights note
structure count
chunk count
concept/pattern/checklist candidate counts
warnings
status
local artifact path (not uploaded if restricted)
```

Statuses:

```text
LOCAL_READY
DOWNLOAD_READY
SOURCE_PENDING
ACQUIRED
STRUCTURED
CHUNKED
REVIEW_READY
BLOCKED_RIGHTS
FAILED
```

## 8. Publication / copyright boundary

- Public source availability does not automatically mean unrestricted republication.
- Original third-party books, paid OTUS materials and restricted PDFs are not duplicated into public GitHub merely for convenience.
- Store such originals locally; publish only metadata, hashes, citations, lawful excerpts/derived notes and original FATHER-created diagrams where appropriate.
- Open-source/CC materials may be mirrored only in accordance with their license and attribution requirements.

## 9. MVP acceptance

MVP is complete when at least:

1. one existing local OTUS lesson file;
2. one public HTML documentation family;
3. one public Git repository/document snapshot;
4. one public PDF/paper

all pass through the same structure/chunk review contract and produce lesson-linked OTUS_KB candidates without changing the P0 legal Knowledge Factory semantics.
