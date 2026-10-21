# TEST PLAN · Telegram Voice Bridge

## Contract tests

- manifest ↔ Agent Kit Registry;
- K0/K1 compatibility;
- trace event schema;
- environment required fields.

## Route tests

1. normal Russian text → voice;
2. punctuation/multiline text → voice;
3. normal Russian voice → text;
4. silence/empty speech → WARN;
5. unsupported photo/document → safe response;
6. Telegram download failure → FAIL trace;
7. TTS provider failure → FAIL trace;
8. STT provider failure → FAIL trace;
9. TRACE_CAPTURE_CONTENT=false → raw content absent.

## Integration

Requires real Telegram bot token and connectivity. Until this run exists, agent remains EXPERIMENTAL.

## Regression

Every fixed runtime failure becomes a regression case.