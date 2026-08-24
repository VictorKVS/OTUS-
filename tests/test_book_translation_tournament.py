from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from book_translation_tournament import choose_samples, score_translation
from book_translate import qc_translation


def test_good_russian_translation_scores_above_untranslated_english() -> None:
    source = "Architects must analyze trade-offs when choosing service granularity in distributed systems."
    good = "Архитекторы должны анализировать компромиссы при выборе гранулярности сервисов в распределённых системах."
    bad = source

    good_qc, good_flags = qc_translation(source, good)
    bad_qc, bad_flags = qc_translation(source, bad)

    assert good_qc == "PASS"
    assert bad_qc == "NEEDS_REVIEW"
    assert score_translation(source, good, good_qc, good_flags) > score_translation(source, bad, bad_qc, bad_flags)


def test_sample_selection_spreads_units_across_book() -> None:
    units = []
    for order in range(1, 101):
        text = (
            "Architecture trade-off coupling cohesion distributed service data granularity. "
            + ("Technical explanation. " * 30)
        )
        units.append({"order": order, "source_text": text, "unit_id": f"u{order}", "source_page_start": order})

    samples = choose_samples(units, 5)
    orders = [int(row["order"]) for row in samples]

    assert len(samples) == 5
    assert min(orders) < 25
    assert max(orders) > 75
