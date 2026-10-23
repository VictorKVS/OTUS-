# Value Delivery Roadmap

| Stage | Purpose | Exit evidence |
|---|---|---|
| Discovery | prove problem/data/access constraints | approved context, REQ/NFR, sample corpus |
| PoC | prove RAG quality hypothesis | golden set + retrieval/faithfulness baseline |
| MVP | build usable controlled service | API/UI, auth, RAG, logging, tests |
| Production Readiness | prove safety/operability | security/eval/SLO/sizing/rollback evidence |
| Production | controlled release | Canary pass + stable promotion |

## No-skip rule

Lesson 2 course material explicitly treats PoC as a risk-reduction stage. For this project production delivery is blocked until evaluation and security gates exist.
