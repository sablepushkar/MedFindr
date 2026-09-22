"""Regression tests for the MedFindr v1.2 SignalGraph pipeline."""
from __future__ import annotations
import unittest
from unittest.mock import patch
from utils.clinical_data import extract_clinical_context
from utils.data_quality import assess_data_quality
from utils.response_engine import build_response
from utils.safety_signals import assess_safety_signal

class SignalGraphTests(unittest.TestCase):
    def test_extracts_structured_symptoms_and_exposure(self):
        context = extract_clinical_context("rash and fever after taking a new medicine", "example")
        concepts = {item.concept for item in context.symptoms}
        self.assertIn("rash", concepts)
        self.assertIn("fever", concepts)
        self.assertEqual(context.temporal_relationship, "after_medication_exposure")

    def test_flags_signal_without_claiming_causality(self):
        context = extract_clinical_context("rash and fever after taking a new medicine", "example")
        signal = assess_safety_signal(context)
        self.assertEqual(signal.status, "flagged")
        self.assertIn("potential medication-related", signal.signal_type)
        self.assertIn("not evidence of causality", signal.explanation)

    def test_medication_without_timing_is_context_incomplete(self):
        context = extract_clinical_context("rash while using a medicine", "example")
        signal = assess_safety_signal(context)
        self.assertEqual(signal.status, "context_incomplete")
        self.assertEqual(signal.priority, "review")

    def test_data_quality_is_explicit(self):
        context = extract_clinical_context("rash after taking a medicine", "example")
        quality = assess_data_quality(context, "example")
        self.assertGreaterEqual(quality.score, 50)
        self.assertIn("temporal medication relationship", quality.present)

    def test_response_contains_trace_evidence_and_signal(self):
        response = build_response("rash and fever after taking a new medicine", "example", include_ebm=False)
        self.assertIsNotNone(response.trace)
        self.assertTrue(response.trace.stages)
        self.assertIsNotNone(response.safety_signal)
        self.assertTrue(response.evidence)
        self.assertIsNotNone(response.data_quality)

    @patch("utils.response_engine.search_drug")
    def test_external_result_becomes_evidence(self, mock_search):
        mock_search.return_value = {
            "status": "success",
            "source": "Test source",
            "source_url": "https://example.test",
            "query": "example",
            "retrieved_at_utc": "2026-09-22T00:00:00+00:00",
        }
        response = build_response("rash", "example", include_ebm=False)
        self.assertTrue(any(item.evidence_type == "regulatory_label" for item in response.evidence))

    def test_trace_has_no_patient_identifier_and_uses_random_analysis_id(self):
        first = build_response("headache", include_ebm=False).to_dict()
        second = build_response("headache", include_ebm=False).to_dict()
        self.assertIn("analysis_id", first["trace"])
        self.assertNotIn("patient_id", first["trace"])
        self.assertRegex(first["trace"]["analysis_id"], r"^MF-[0-9a-f]{12}$")
        self.assertNotEqual(first["trace"]["analysis_id"], second["trace"]["analysis_id"])

if __name__ == "__main__":
    unittest.main()
