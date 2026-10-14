"""Regression tests for experimental-model feature extraction boundaries."""
from __future__ import annotations
import unittest
from utils.ebm_risk import extract_features

class EBMFeatureTests(unittest.TestCase):
    def test_direct_negations_do_not_set_present_symptom_features(self):
        features = extract_features("no chest pain, denies difficulty breathing, and no fever")
        self.assertEqual(features["has_chest_pain"], 0)
        self.assertEqual(features["has_breathing"], 0)
        self.assertEqual(features["has_fever"], 0)

    def test_negation_does_not_cross_conjunction(self):
        features = extract_features("no chest pain but fever")
        self.assertEqual(features["has_chest_pain"], 0)
        self.assertEqual(features["has_fever"], 1)

    def test_blood_pressure_is_not_misread_as_bleeding(self):
        self.assertEqual(extract_features("my blood pressure is normal")["has_bleeding"], 0)
        self.assertEqual(extract_features("blood in stool")["has_bleeding"], 1)

    def test_duration_is_extracted_in_days(self):
        self.assertEqual(extract_features("headache for 2 weeks")["duration_days"], 14)
        self.assertEqual(extract_features("fever for 48 hours")["duration_days"], 2)
        self.assertEqual(extract_features("headache")["duration_days"], 0)

if __name__ == "__main__":
    unittest.main()
