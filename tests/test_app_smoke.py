"""Smoke-test the Streamlit UI and its session-scoped review export."""
from __future__ import annotations

import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


class AppSmokeTests(unittest.TestCase):
    def _run(self, app):
        app.run()
        errors = [str(item.value) for item in app.exception]
        self.assertEqual(errors, [], "Streamlit app raised during render: " + "; ".join(errors))

    def _click(self, app, label):
        button = next((item for item in app.button if item.label == label), None)
        self.assertIsNotNone(button, f"Missing button: {label}")
        button.click()
        self._run(app)

    def test_application_renders_without_streamlit_exceptions(self):
        app_path = Path(__file__).resolve().parents[1] / "app.py"
        app = AppTest.from_file(str(app_path), default_timeout=20)
        self._run(app)
        self.assertTrue(any(item.label == "Health concern" for item in app.text_area))
        self.assertTrue(any(item.label == "Optional drug name" for item in app.text_input))

    def test_review_bundle_survives_review_form_rerun(self):
        app_path = Path(__file__).resolve().parents[1] / "app.py"
        app = AppTest.from_file(str(app_path), default_timeout=20)
        self._run(app)
        concern = next(item for item in app.text_area if item.label == "Health concern")
        concern.set_value("rash and fever after taking a new medicine")
        self._click(app, "Generate structured view")
        self.assertIn("last_response", app.session_state)
        self._click(app, "Validate review and prepare JSON export")
        response = app.session_state["last_response"]
        bundle_key = f"review_bundle_{response.trace.analysis_id}"
        self.assertIn(bundle_key, app.session_state)
        self.assertTrue(app.session_state[bundle_key])


if __name__ == "__main__":
    unittest.main()
