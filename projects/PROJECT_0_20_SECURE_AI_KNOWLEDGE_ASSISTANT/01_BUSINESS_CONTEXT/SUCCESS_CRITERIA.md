# Success Criteria & Measurement Plan

| ID | Критерий | Метод | Статус |
|---|---|---|---|
| BUS-01 | снизить время получения подтверждённого ответа | paired task study: manual vs AI | DESIGN, target TBD after baseline |
| BUS-02 | пользователь видит источник ответа | automated citation presence + human check | DESIGN |
| QLT-01 | ответ опирается на retrieved context | faithfulness/groundedness eval | DESIGN |
| QLT-02 | retrieval находит релевантные документы | retrieval recall/precision on golden set | DESIGN |
| SEC-01 | ACL не допускает retrieval запрещённого документа | adversarial access test | MUST |
| SEC-02 | критическая утечка секретов/PII не проходит release gate | security regression suite | MUST |
| OPS-01 | релиз воспроизводим | image/model/index/prompt immutable refs | MUST |
| OPS-02 | rollback выполняется без rebuild stable | canary rollback drill | MUST |

## Course NFR values

В Lesson 2 приложен **шаблон** NFR с примерами: TTFT <1.5 s, p95 <5 s, >50 RPS, 100 concurrent sessions, Answer Relevancy >0.85, Faithfulness >0.9, Context Recall >0.8 и др.

Для SAIKA эти значения хранятся как `COURSE_TEMPLATE`, а не как доказанный target. На этапах 13/15/16/17 они проходят calibration и только после этого могут стать project SLO/NFR.
