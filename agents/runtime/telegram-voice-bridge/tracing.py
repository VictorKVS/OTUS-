from __future__ import annotations

import json
import os
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

AGENT_ID = "FTH-AG-VBR-001"

class TraceWriter:
    def __init__(self, path: Path, capture_content: bool = False) -> None:
        self.path = path
        self.capture_content = capture_content
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def new_trace_id(self) -> str:
        return f"vbr-{uuid.uuid4().hex[:16]}"

    def event(
        self,
        trace_id: str,
        event: str,
        status: str,
        *,
        duration_ms: float | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        payload = {
            "trace_id": trace_id,
            "event_id": uuid.uuid4().hex,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agent_id": AGENT_ID,
            "event": event,
            "status": status,
            "duration_ms": duration_ms,
            "metadata": metadata or {},
        }
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")

    def text_meta(self, text: str) -> dict[str, Any]:
        if self.capture_content:
            return {"text": text, "text_chars": len(text)}
        return {"text_chars": len(text), "content_redacted": True}

class Timer:
    def __enter__(self):
        self.started = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.duration_ms = round((time.perf_counter() - self.started) * 1000, 2)

def bool_env(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}