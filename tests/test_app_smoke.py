"""Smoke-test the real Streamlit script in its supported test harness."""
from __future__ import annotations

import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


class AppSmokeTests(unittest.TestCase):
    def test_application_renders_without_streamlit_exceptions(self):
        app_path = Path(__file__).resolve().parents[1] / "app.py"
        app = AppTest.from_file(str(app_path), default_timeout=20).run()
        errors = [str(item.value) for item in app.exception]
        self.assertEqual(errors, [], "Streamlit app raised during initial render: " + "; ".join(errors))
        self.assertTrue(any(item.label == "Health concern" for item in app.text_area))
        self.assertTrue(any(item.label == "Optional drug name" for item in app.text_input))


if __name__ == "__main__":
    unittest.main()
