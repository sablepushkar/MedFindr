"""Regression tests for the MedFindr v2 human review workflow."""
from __future__ import annotations
import json
import unittest
from utils.review import create_review_record, validate_review_record
from utils.review_export import build_review_bundle, serialize_review_bundle
from utils.response_engine import build_response
class ReviewWorkflowTests(unittest.TestCase):
    def test_review_record_starts_from_analysis(self):
        response = build_response("rash and fever after taking a new medicine", include_ebm=False)
        review = create_review_record(response)
        self.assertRegex(review.analysis_id, r"^MF-[0-9a-f]{12}$")
        self.assertTrue(review.missing_information)
        self.assertEqual(review.status, "new")
    def test_review_validation_requires_follow_up_notes(self):
        review = create_review_record(build_response("rash", include_ebm=False))
        review.follow_up_required = True
        self.assertIn("Follow-up notes are required", " ".join(validate_review_record(review)))
    def test_review_can_be_marked_reviewed(self):
        review = create_review_record(build_response("headache", include_ebm=False))
        review.status = "in_review"; review.reviewer_reasoning = "Reviewed the prototype signal and available context."; review.disposition = "informational"
        review.mark_reviewed()
        self.assertEqual(review.status, "reviewed"); self.assertTrue(review.reviewed_at_utc)
    def test_bundle_contains_analysis_and_review(self):
        response = build_response("rash after taking a new medicine", include_ebm=False); review = create_review_record(response)
        bundle = build_review_bundle(response, review)
        self.assertEqual(bundle["format"], "medfindr-review-bundle"); self.assertEqual(bundle["format_version"], "2.0")
        self.assertIn("analysis", bundle); self.assertIn("review", bundle)
        parsed = json.loads(serialize_review_bundle(response, review)); self.assertEqual(parsed["review"]["analysis_id"], review.analysis_id)
    def test_review_bundle_does_not_create_patient_id(self):
        response = build_response("headache", include_ebm=False); review = create_review_record(response)
        self.assertNotIn("patient_id", json.dumps(build_review_bundle(response, review)))
if __name__ == "__main__": unittest.main()
