import unittest
from datetime import datetime
from unittest.mock import Mock, patch

import requests

from utils.drug_lookup import search_drug


class DrugLookupReliabilityTests(unittest.TestCase):
    def make_response(self, status_code=200, payload=None):
        response = Mock()
        response.status_code = status_code
        response.json.return_value = payload or {
            "results": [{
                "openfda": {
                    "brand_name": ["ExampleBrand"],
                    "generic_name": ["example ingredient"],
                    "manufacturer_name": ["Example Manufacturer"],
                    "route": ["ORAL"],
                    "product_type": ["HUMAN PRESCRIPTION DRUG"],
                },
                "warnings": ["Read the source label."],
            }]
        }
        response.raise_for_status.return_value = None
        return response

    @patch("utils.drug_lookup.requests.get")
    def test_success_contains_source_and_timezone_aware_retrieval_time(self, get):
        get.return_value = self.make_response()
        result = search_drug("ExampleBrand")
        self.assertEqual(result["status"], "success")
        self.assertIn("OpenFDA", result["source"])
        self.assertTrue(result["source_url"].startswith("https://"))
        self.assertEqual(result["brand_name"], "ExampleBrand")
        retrieved = datetime.fromisoformat(result["retrieved_at_utc"])
        self.assertIsNotNone(retrieved.utcoffset())
        get.assert_called_once()

    @patch("utils.drug_lookup.requests.get")
    def test_not_found_is_an_explicit_state(self, get):
        get.return_value = self.make_response(status_code=404)
        result = search_drug("ExampleBrand")
        self.assertEqual(result["status"], "not_found")
        self.assertIn("retrieved_at_utc", result)
        self.assertIn("source_url", result)

    @patch("utils.drug_lookup.requests.get")
    def test_timeout_returns_bounded_error_and_provenance(self, get):
        get.side_effect = requests.Timeout()
        result = search_drug("ExampleBrand")
        self.assertEqual(result["status"], "error")
        self.assertIn("retrieved_at_utc", result)
        self.assertNotIn("Traceback", result["message"])

    @patch("utils.drug_lookup.requests.get")
    def test_malformed_json_returns_explicit_error(self, get):
        response = self.make_response()
        response.json.side_effect = ValueError("not json")
        get.return_value = response
        result = search_drug("ExampleBrand")
        self.assertEqual(result["status"], "error")
        self.assertIn("invalid response", result["message"])

    @patch("utils.drug_lookup.requests.get")
    def test_unexpected_payload_shape_is_rejected(self, get):
        get.return_value = self.make_response(payload={"results": ["bad record"]})
        result = search_drug("ExampleBrand")
        self.assertEqual(result["status"], "error")

    @patch("utils.drug_lookup.requests.get")
    def test_invalid_input_never_calls_external_service(self, get):
        result = search_drug("x")
        self.assertEqual(result["status"], "error")
        get.assert_not_called()


if __name__ == "__main__":
    unittest.main()
