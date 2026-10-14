import unittest

from scripts.evaluate_signals import build_report, evaluate_cases, validate_cases


class SignalEvaluationTests(unittest.TestCase):
    def setUp(self):
        self.cases = [
            {
                "id": "case-1",
                "concern": "rash and fever after taking a new medicine",
                "drug_name": "ExampleMedicine",
                "expected_status": "flagged",
            }
        ]

    def test_report_has_fixture_fingerprint_and_scope(self):
        raw = b'[{"id":"case-1"}]'
        report = build_report(self.cases, raw, "fixture.json")
        self.assertEqual(report["fixture"]["path"], "fixture.json")
        self.assertEqual(len(report["fixture"]["sha256"]), 64)
        self.assertIn("not clinical", report["evaluation_scope"])
        self.assertIn("source_revision", report)

    def test_report_fingerprint_changes_when_fixture_changes(self):
        first = build_report(self.cases, b"fixture-a")
        second = build_report(self.cases, b"fixture-b")
        self.assertNotEqual(first["fixture"]["sha256"], second["fixture"]["sha256"])

    def test_duplicate_ids_are_rejected(self):
        cases = self.cases + [dict(self.cases[0])]
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            validate_cases(cases)

    def test_blank_concern_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "non-empty concern"):
            validate_cases([{**self.cases[0], "concern": "  "}])

    def test_unknown_expected_status_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "unknown expected_status"):
            validate_cases([{**self.cases[0], "expected_status": "certain"}])

    def test_evaluator_returns_case_level_mismatches(self):
        report = evaluate_cases(self.cases)
        self.assertEqual(report["case_count"], 1)
        self.assertIn("mismatches", report)
        self.assertIn("agreement_percent", report)


if __name__ == "__main__":
    unittest.main()
