"""Regression and contract tests for MedFindr v1.1."""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from utils.drug_lookup import search_drug
from utils.response_engine import build_response
from utils.urgency import assess_urgency
from utils.validation import validate_concern, validate_drug_name

ROOT = Path(__file__).resolve().parents[1]
EVAL_PATH = ROOT / "data" / "evaluation_set.json"


class ValidationTests(unittest.TestCase):
    def test_empty_concern_is_rejected(self):
        result = validate_concern("")
        self.assertFalse(result.valid)

    def test_concern_length_is_bounded(self):
        result = validate_concern("x" * 2001)
        self.assertFalse(result.valid)

    def test_control_characters_are_removed(self):
        result = validate_concern("fever\x00 today")
        self.assertTrue(result.valid)
        self.assertNotIn("\x00", result.value)

    def test_drug_name_length_is_bounded(self):
        result = validate_drug_name("x" * 121)
        self.assertFalse(result.valid)


class UrgencyRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with EVAL_PATH.open("r", encoding="utf-8") as handle:
            cls.cases = json.load(handle)

    def test_evaluation_set_matches_expected_labels(self):
        failures = []
        for item in self.cases:
            result = assess_urgency(item["concern"])
            expected = item["expected_urgency"].strip().lower()
            if result.level != expected:
                failures.append(
                    f'{item.get("id", "<unknown>")}: expected {expected}, got {result.level}'
                )
        self.assertEqual([], failures, "\n".join(failures))

    def test_empty_input_is_handled(self):
        result = assess_urgency("")
        self.assertEqual(result.level, "low")
        self.assertEqual(result.score, 0)
        self.assertTrue(result.reasons)

    def test_high_flag_produces_high_urgency(self):
        result = assess_urgency("sudden chest pain")
        self.assertEqual(result.level, "high")
        self.assertGreaterEqual(result.score, 10)

    def test_high_combination_rule(self):
        self.assertEqual(
            assess_urgency("high fever with rash and severe headache").level,
            "high",
        )

    def test_contextual_swelling_case_remains_low(self):
        self.assertEqual(
            assess_urgency("ankle swelling after standing all day").level,
            "low",
        )

    def test_reasons_are_not_duplicated(self):
        result = assess_urgency("chest pain and chest pain")
        self.assertEqual(len(result.reasons), len(set(result.reasons)))


class DrugLookupTests(unittest.TestCase):
    def test_short_drug_name_is_rejected_without_network(self):
        with patch("utils.drug_lookup.requests.get") as mock_get:
            result = search_drug("x")
        mock_get.assert_not_called()
        self.assertEqual(result["status"], "error")

    @patch("utils.drug_lookup.requests.get")
    def test_malformed_api_json_is_handled(self, mock_get):
        response = Mock(status_code=200)
        response.json.side_effect = ValueError("bad json")
        response.raise_for_status.return_value = None
        mock_get.return_value = response

        result = search_drug("example")
        self.assertEqual(result["status"], "error")
        self.assertNotIn("detail", result)

    @patch("utils.drug_lookup.requests.get")
    def test_success_result_contains_provenance(self, mock_get):
        response = Mock(status_code=200)
        response.json.return_value = {
            "results": [
                {
                    "openfda": {
                        "brand_name": ["Example"],
                        "generic_name": ["example"],
                        "manufacturer_name": ["Example Labs"],
                    },
                    "warnings": ["Use according to the official label."],
                }
            ]
        }
        response.raise_for_status.return_value = None
        mock_get.return_value = response

        result = search_drug("example")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["source_type"], "retrieved")
        self.assertIn("source_url", result)
        self.assertIn("retrieved_at_utc", result)


class ResponseEngineTests(unittest.TestCase):
    @patch("utils.response_engine.search_drug")
    def test_response_pipeline_is_structured(self, mock_search):
        mock_search.return_value = {"status": "success", "query": "example"}
        response = build_response("sudden chest pain", drug_name="example")
        self.assertEqual(response.urgency.level, "high")
        self.assertTrue(response.sections)
        self.assertEqual(response.drug_result["status"], "success")
        self.assertEqual(response.to_dict()["urgency"]["level"], "high")
        self.assertFalse(response.errors)

    def test_invalid_concern_stops_analysis(self):
        response = build_response(" ")
        self.assertTrue(response.errors)
        self.assertEqual(response.sections[0].level, "error")

    def test_response_can_disable_ebm(self):
        response = build_response("headache", include_ebm=False)
        self.assertIsNone(response.ebm)
        self.assertEqual(response.urgency.level, "low")


if __name__ == "__main__":
    unittest.main()
