# Sequence · Query with citations

```text
USER
  ↓ question
API
  ↓ validate
IDENTITY CONTEXT
  ↓ subject/roles
POLICY ENGINE
  ↓ allowed scope
RETRIEVER
  ↓ authorized chunks + scores
CONTEXT BUILDER
  ↓ bounded evidence context
MODEL ADAPTER
  ↓ draft answer
OUTPUT VALIDATOR
  ↓ grounded/security/citation check
AUDIT
  ↓ trace event
API
  ↓ answer + citations + release_id
USER
```

No diagonal/crossing connector is used in the canonical view. Alternative/failure sequences are separate documents to keep diagrams readable.
