from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from book_translate import qc_translation
from translation_model_policy import reject_reason


def test_llava_is_rejected_for_book_translation() -> None:
    assert reject_reason("llava:7b") is not None


def test_mixed_transliteration_does_not_pass_as_russian_translation() -> None:
    source = "Software Architecture: The Hard Parts Modern Trade-Off Analyses for Distributed Architectures"
    target = "Софтвере architeктуре: The Hard Parts Modern Trade-Off Analyses for Distributed Architectures"
    status, flags = qc_translation(source, target)
    assert status == "NEEDS_REVIEW"
    assert "LOW_CYRILLIC_SHARE" in flags or "EXCESSIVE_LATIN_TEXT" in flags


def test_source_mostly_retained_after_translation_prefix_is_rejected() -> None:
    source = (
        "This book provides the missing manual around building microservices and analyzing "
        "the nuances of architectural decisions throughout the whole tech stack."
    )
    target = "Перевод: " + source
    status, flags = qc_translation(source, target)
    assert status == "NEEDS_REVIEW"
    assert "SOURCE_TEXT_LARGELY_RETAINED" in flags or "EXCESSIVE_LATIN_TEXT" in flags


def test_real_russian_translation_can_pass_basic_script_gate() -> None:
    source = "Architects must analyze trade-offs when choosing a distributed architecture."
    target = "Архитекторы должны анализировать компромиссы при выборе распределённой архитектуры."
    status, flags = qc_translation(source, target)
    assert status == "PASS"
    assert flags == []
