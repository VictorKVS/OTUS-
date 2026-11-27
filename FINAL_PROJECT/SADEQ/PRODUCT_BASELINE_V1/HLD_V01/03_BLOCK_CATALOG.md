# HLD-BLOCKS-001 — Блоки, responsibility boundaries and information contracts (draft)
**Rule:** every block receives only explicitly approved fields. Before LLD, bind `ALG, CMP, FLOW, SEC, THR, TEST` identifiers; no arbitrary `payload` across trusted boundaries.

| ID | Block | Owns | Input contract (logical) | Output contract (logical) | Does NOT own |
|---|---|---|---|---|---|
| B01 | Integration & Security Gateway | source validation, routing, auth context, allowlisted external adapters | `SourceEnvelope` + verified identity | `ValidatedObservation` or `Reject` | entity identity decisions, action approval |
| B02 | Object & Event Core | entity resolution, append-only events, snapshots, replay | `ValidatedObservation`, `ResolutionRule` | `ObjectEvent`, `StateVersion`, `ProvenanceRef` | LLM self-modification, external tool effects |
| B03 | Knowledge & Evidence | source provenance, indexing, authorized GraphRAG, evidence | `EvidenceQuery + AuthContext`, `ApprovedSource` | `EvidenceBundle` with graph path and source ref | action authorization or autonomous source trust |
| B04 | Intelligence & Orchestration | LangGraph finite workflow, algorithm selection, forecast with backtest, proposal | `StateVersion`, `EvidenceBundle`, `AgentProfile` | `AnalysisResult`, `ActionProposalDraft` or `ABSTAIN` | final policy, self-grant, final QA |
| B05 | Decision & Action Control | policy evaluation, impact constraints, approval, idempotent authorized tool call | `ActionProposalDraft`, `VerifiedIdentity`, `QualifiedVersion` | `PolicyDecision`, `ExecutionReceipt`, `DENY` | alter model, approve own rules |
| B06 | Agent Factory & Registry | profile templates, domain packs, build proposal, version registry | `MissionSpec`, `ApprovedAlgorithms`, `ToolContract` | `CandidateAgentManifest` and test plan | qualification or production release |
| B07 | Independent POLYGON | heldout suite, security+quality exam, proposed trust/revocation | `CandidateAgentManifest`, `ImmutableTestCorpus` | `QualificationEvidence`, `PASS/FAIL` recommendation | candidate mutation, self-approval |
| B08 | Platform & Operations | deployment, storage, local AI serving, telemetry, rollback and incident | `ApprovedReleaseManifest`, `OperationalPolicy` | `RuntimeState`, `Trace`, `AuditRef`, `Incident` | release decision without human authority |

## Central invariants
**INV-01:** no unknown input/output fields, recipients or tool types at all trust boundaries.  
**INV-02:** every action is checked by B05 *after* B04 proposes it and before execution.  
**INV-03:** B07 cannot modify candidate, and candidate cannot modify B07 test criteria.  
**INV-04:** only B02 owns canonical object/event identity and state; vectors/graph are projections, not Source of Truth.  
**INV-05:** B04 may explain/recommend, but forecasts must expose reproducible algorithm/backtest.  
**INV-06:** all storage/inference within strict offline deployment for OTUS.  
**INV-07:** tenant data isolation across caches, graph edges, vectors, citations and logs.  
**INV-08:** agent memory persists through Pod restart; process state is not local single Pod memory.

## Interfaces to detail at LLD
- FLOW-01: B01→B02 observation envelope (closed schemas per source+kind+version).
- FLOW-02: B02→B04 state/event reference (immutable event and object versions).
- FLOW-03: B04→B03 authenticated query → evidence refs; no direct retrieval bypass.
- FLOW-04: B04→B05 action proposal + context, no write permission conveyed.
- FLOW-05: B05→approved tool via B01/Tool Gateway, with revalidated approval and action hash.
- FLOW-06: B06→B07 immutable candidate + declared qualification suite; human approval remains independent.
- FLOW-07: B07→B08 signed evidence→human release gate; no direct deploy by candidate.
- FLOW-08: B08→B07 change/requalification signal for new model, data, tool, policy or image.

## Explicit separation from LLD
These are **logical** contract names, not fully specified JSON Schema. Current OpenAPI v0.1 has known overly broad nested `payload` fields and is NOT contract-strict. Next step: choose FLOW-01 and FLOW-02 and produce executable schemas and tests without implementing unrelated endpoints.
