import unittest
from pathlib import Path

from scripts.inventory_gost_ib_library import match_seed


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


if __name__ == "__main__":
    unittest.main()
