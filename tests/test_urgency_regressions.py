from __future__ import annotations

import unittest

from utils.urgency import assess_urgency
from utils.validation import validate_concern, validate_drug_name


class UrgencyRegressionTests(unittest.TestCase):
    def test_specific_moderate_phrase_is_not_double_counted(self):
        high_fever = assess_urgency("high fever")
        self.assertEqual(high_fever.score, 3)
        self.assertIn("High fever", high_fever.reasons)
        self.assertNotIn("Fever present", high_fever.reasons)

    def test_persistent_vomiting_is_not_double_counted(self):
        result = assess_urgency("persistent vomiting")
        self.assertEqual(result.score, 3)
        self.assertIn("Persistent vomiting", result.reasons)
        self.assertNotIn("Vomiting", result.reasons)

    def test_distinct_moderate_signals_still_accumulate(self):
        result = assess_urgency("fever and dizziness")
        self.assertEqual(result.score, 6)
        self.assertEqual(result.level, "moderate")

    def test_existing_input_limits_remain_enforced(self):
        self.assertFalse(validate_concern("  ").valid)
        self.assertFalse(validate_drug_name("x").valid)
        self.assertTrue(validate_drug_name("aspirin").valid)


if __name__ == "__main__":
    unittest.main()
