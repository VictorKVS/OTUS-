# FTH-CMP-TELEGRAM-CHANNEL-001

Reusable Telegram transport block extracted from the FATHER_VOICE_BRIDGE reference product.

Current state: **EXPERIMENTAL / EXTRACTION_IN_PROGRESS**.

The block is deliberately narrower than the Voice Bridge agent:

```text
Telegram Bot API
   ↓
receive / authorize / normalize
   ↓
MESSAGE EVENT
   ↓
other FATHER blocks
   ↓
send text / send voice
```

It must not contain ALINA reasoning, RAG logic, model routing or TTS/STT business logic.
