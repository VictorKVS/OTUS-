from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from book_translation_jury import parse_json_object, weighted_score


def test_parse_json_object_accepts_fenced_json() -> None:
    payload = parse_json_object(
        '```json\n{"scores":{"A":{"adequacy":9,"terminology":8,"completeness":9,"fluency":8,"structure":9}},"winner":"A","reason":"ok"}\n```'
    )
    assert payload["winner"] == "A"
    assert payload["scores"]["A"]["adequacy"] == 9


def test_weighted_score_prioritizes_adequacy_and_terminology() -> None:
    strong = weighted_score(
        {
            "adequacy": 10,
            "terminology": 10,
            "completeness": 9,
            "fluency": 7,
            "structure": 8,
        }
    )
    weak = weighted_score(
        {
            "adequacy": 5,
            "terminology": 5,
            "completeness": 10,
            "fluency": 10,
            "structure": 10,
        }
    )
    assert strong > weak
