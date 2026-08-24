from __future__ import annotations

REJECT_MODEL_MARKERS = (
    "llava",
    "vision",
    "cogvlm",
    "minicpm-v",
    "qwen-vl",
    "qwen2-vl",
    "qwen2.5-vl",
    "internvl",
    "bakllava",
)

PREFERRED_MODEL_MARKERS = (
    "qwen",
    "gigachat",
    "mistral",
    "llama",
    "gemma",
    "phi",
    "deepseek",
)


def reject_reason(model_id: str) -> str | None:
    normalized = model_id.casefold().strip()
    if not normalized:
        return "EMPTY_MODEL_ID"
    for marker in REJECT_MODEL_MARKERS:
        if marker in normalized:
            return f"UNSUITABLE_VISION_MODEL:{marker}"
    return None


def rank_model(model_id: str) -> tuple[int, str]:
    reason = reject_reason(model_id)
    if reason:
        return (-1000, model_id.casefold())
    normalized = model_id.casefold()
    score = 0
    for index, marker in enumerate(PREFERRED_MODEL_MARKERS):
        if marker in normalized:
            score += 100 - index
    if "instruct" in normalized:
        score += 40
    if "chat" in normalized:
        score += 20
    return (score, normalized)
