# LLD · Query API Container

Lesson 5 asks to detail one HLD container to components, sequence and OpenAPI. We detail the Query API / Orchestrator path.

## Components

| Component | Responsibility |
|---|---|
| RequestValidator | schema/size/basic validation |
| IdentityContextAdapter | normalize subject/roles/claims |
| PolicyEngine | authorize requested knowledge scope |
| QueryNormalizer | normalize user query |
| RetrieverClient | call retrieval contract |
| ContextBuilder | select/budget chunks |
| ModelClient | provider-independent generation |
| OutputValidator | groundedness/security/citation policy |
| AuditEmitter | structured event emission |

## Main sequence

```text
Client
→ API: POST /v1/query
→ RequestValidator
→ IdentityContextAdapter
→ PolicyEngine
→ RetrieverClient
→ ContextBuilder
→ ModelClient
→ OutputValidator
→ AuditEmitter
→ Client: answer + citations + trace_id
```

## Failure paths

- invalid request → 400;
- unauthenticated → 401;
- forbidden scope → 403;
- insufficient evidence → 200 with `answer_status=insufficient_evidence`;
- upstream model timeout → 503 with trace_id;
- policy/security block → 422/403 according to policy class, with no sensitive details.
