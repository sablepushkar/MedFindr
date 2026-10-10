import unittest

from scripts.evaluate import build_report, evaluate


class EvaluationWorkflowTests(unittest.TestCase):
    def test_evaluation_returns_machine_readable_metrics(self):
        results, confusion = evaluate([
            {"id": "low-1", "concern": "seasonal sneezing", "expected_urgency": "low"},
            {"id": "high-1", "concern": "difficulty breathing", "expected_urgency": "high"},
        ])
        report = build_report(results, confusion)
        self.assertEqual(report["project_version"], "MedFindr X2")
        self.assertEqual(report["total_cases"], 2)
        self.assertEqual(report["correct_cases"], 2)
        self.assertEqual(report["accuracy_percent"], 100.0)
        self.assertEqual(report["per_class"]["high"]["support"], 1)

    def test_unknown_expected_label_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "unknown expected_urgency"):
            evaluate([{"id": "bad", "concern": "some concern", "expected_urgency": "urgent"}])

    def test_blank_concern_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "non-empty concern"):
            evaluate([{"id": "blank", "concern": "  ", "expected_urgency": "low"}])

    def test_duplicate_case_ids_are_rejected(self):
        cases = [
            {"id": "same", "concern": "sneezing", "expected_urgency": "low"},
            {"id": "same", "concern": "difficulty breathing", "expected_urgency": "high"},
        ]
        with self.assertRaisesRegex(ValueError, "Duplicate evaluation case id"):
            evaluate(cases)


if __name__ == "__main__":
    unittest.main()
