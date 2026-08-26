import tempfile
import unittest
from pathlib import Path

from scripts.inventory_gost_ib_library import (
    content_seed_candidate,
    has_standard_hint,
    is_reference_list,
    match_seed,
)


SEED = [
    "ГОСТ Р 56939-2024",
    "ГОСТ Р 59453.1-2021",
    "ГОСТ Р ИСО/МЭК 15408-1-2012",
]


class GostInventoryMatchingTests(unittest.TestCase):
    def test_exact_designation_with_title_suffix(self):
        match, basis, confidence = match_seed(Path("ГОСТ Р 56939-2024 безопасная разработка.pdf"), SEED)
        self.assertEqual(match, "ГОСТ Р 56939-2024")
        self.assertEqual(confidence, "HIGH")

    def test_underscores_and_latin_prefix_are_tolerated(self):
        match, basis, confidence = match_seed(Path("GOST_R_56939_2024.pdf"), SEED)
        self.assertEqual(match, "ГОСТ Р 56939-2024")
        self.assertIn(confidence, {"HIGH", "MEDIUM"})

    def test_code_only_filename_is_tolerated(self):
        match, basis, confidence = match_seed(Path("56939-2024.pdf"), SEED)
        self.assertEqual(match, "ГОСТ Р 56939-2024")

    def test_part_number_is_not_collapsed(self):
        match, basis, confidence = match_seed(Path("ГОСТ_Р_59453.1_2021.pdf"), SEED)
        self.assertEqual(match, "ГОСТ Р 59453.1-2021")

    def test_unrelated_number_is_not_promoted(self):
        match, basis, confidence = match_seed(Path("invoice_56939_2024_777.pdf"), SEED)
        self.assertIsNone(match)
        self.assertEqual(confidence, "NONE")

    def test_iso_substring_inside_book_author_or_word_is_not_standard_hint(self):
        self.assertFalse(has_standard_hint(Path("Dave_Harrison_Knox_Lively_Achieving.pdf")))
        self.assertFalse(has_standard_hint(Path("David-Farley-Addison-Wesley.pdf")))
        self.assertFalse(has_standard_hint(Path("Создание микросервисов.pdf")))

    def test_real_standard_markers_are_detected(self):
        self.assertTrue(has_standard_hint(Path("ISO_27001_security.pdf")))
        self.assertTrue(has_standard_hint(Path("ГОСТ Р безопасная разработка.rtf")))

    def test_national_standard_list_is_reference_not_standard(self):
        self.assertTrue(is_reference_list(Path("Перечень национальных стандартов.pdf")))

    def test_rtf_content_surfaces_review_candidate_without_promoting(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "Защита информации. Общие требования. ГОСТ Р.rtf"
            path.write_text(r"{\rtf1 Some header ГОСТ Р 56939-2024 safe software}", encoding="utf-8")
            designation, count, basis = content_seed_candidate(path, SEED)
            self.assertEqual(designation, "ГОСТ Р 56939-2024")
            self.assertEqual(count, 1)
            self.assertEqual(basis, "CONTENT_CODE_PREFIX_REVIEW")


if __name__ == "__main__":
    unittest.main()
