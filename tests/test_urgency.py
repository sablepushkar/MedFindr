"""Regression tests for MedFindr's transparent urgency engine.

These tests protect the known X1.0 evaluation behaviour while V2 work is added.
They intentionally test the rule-based layer only; they are not clinical validation.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from utils.urgency import assess_urgency

ROOT = Path(__file__).resolve().parents[1]
EVAL_PATH = ROOT / "data" / "evaluation_set.json"


class UrgencyRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with EVAL_PATH.open("r", encoding="utf-8") as handle:
            cls.cases = json.load(handle)

    def test_evaluation_set_matches_expected_labels(self) -> None:
        failures = []
        for item in self.cases:
            result = assess_urgency(item["concern"])
            expected = item["expected_urgency"].strip().lower()
            if result.level != expected:
                failures.append(
                    f'{item.get("id", "<unknown>")}: expected {expected}, got {result.level}'
                )
        self.assertEqual([], failures, "\n".join(failures))

    def test_empty_input_is_handled(self) -> None:
        result = assess_urgency("")
        self.assertEqual(result.level, "low")
        self.assertEqual(result.score, 0)
        self.assertTrue(result.reasons)

    def test_high_flag_produces_high_urgency(self) -> None:
        result = assess_urgency("sudden chest pain")
        self.assertEqual(result.level, "high")
        self.assertGreaterEqual(result.score, 10)

    def test_reasons_are_not_duplicated(self) -> None:
        result = assess_urgency("chest pain and chest pain")
        self.assertEqual(len(result.reasons), len(set(result.reasons)))


if __name__ == "__main__":
    unittest.main()
