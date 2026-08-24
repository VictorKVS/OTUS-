# Specialized translation candidates for architecture books

## Goal

Benchmark purpose-built machine-translation models against the current general-LLM tournament on the same EN→RU architecture-book samples.

## Production candidates

### `google/madlad400-3b-mt`

- role: primary specialized MT challenger;
- task: multilingual machine translation;
- target prefix for Russian: `<2ru>`;
- licence: Apache-2.0;
- production eligibility: YES, subject to normal model/package review;
- rationale: translation-specific model, document-oriented training corpus, materially smaller than 7B/10B variants.

### `Helsinki-NLP/opus-mt-en-ru`

- role: lightweight bilingual baseline;
- task: English → Russian machine translation;
- licence: Apache-2.0;
- production eligibility: YES, subject to normal model/package review;
- rationale: small dedicated EN→RU translator; useful speed/quality baseline.

## Research-only benchmark

### `facebook/nllb-200-distilled-1.3B`

- role: multilingual MT benchmark;
- source language: `eng_Latn`;
- target language: `rus_Cyrl`;
- licence: CC-BY-NC-4.0;
- production eligibility: NO for a commercial product without separate rights review;
- rationale: strong translation-specific comparison point.

## Document structure is a separate layer

Do not ask a translation model to reconstruct document layout from flattened text.

Preferred flow:

```text
PDF / EPUB / DOCX
        ↓
Docling document parsing
        ↓
lossless document JSON
        ├─ paragraphs
        ├─ headings
        ├─ lists
        ├─ tables / cells / spans
        ├─ code
        ├─ formulas
        ├─ captions
        └─ figures
        ↓
translate text-bearing nodes only
        ↓
rebuild bilingual structured document
        ↓
semantic units
        ↓
Knowledge Analyst
```

For tables, lossless JSON/HTML is preferred over Markdown because merged-cell structure can be flattened in Markdown serialization.

## Benchmark policy

All specialized MT models must receive the same source samples already used by the general-LLM tournament.

Scoring is not treated as semantic truth. It is used for:

- fail-closed rejection of untranslated or corrupted output;
- completeness checks;
- script/language checks;
- length sanity;
- retained-source detection;
- deterministic ranking.

Near-ties must go to blind jury or human review.
