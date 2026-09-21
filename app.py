"""
MedFindr - Main application entry point.
Version: 07.1 dev

Interface is intentionally kept minimal and stable.
Business logic will be moved out in later steps.
"""

from __future__ import annotations

import json
import logging
from typing import Any

import streamlit as st

from config import (
    APP_CAPTION,
    APP_NAME,
    APP_VERSION,
    DISCLAIMER,
    SAMPLE_CONCERNS_PATH,
)
from utils.drug_lookup import search_drug

# Basic logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_sample_concerns() -> list[dict[str, Any]]:
    """Load sample concerns safely."""
    try:
        with open(SAMPLE_CONCERNS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        return []
    except Exception as exc:
        logger.warning("Could not load sample concerns: %s", exc)
        return []


def main() -> None:
    st.set_page_config(
        page_title=f"{APP_NAME} {APP_VERSION}",
        page_icon="🩺",
        layout="centered",
    )

    st.title(APP_NAME)
    st.caption(f"{APP_VERSION} · {APP_CAPTION}")

    st.warning(DISCLAIMER)

    samples = load_sample_concerns()

    # --- Input section ---
    concern = st.text_area(
        "Describe the health concern",
        placeholder="Example: mild headache and body ache for 2 days",
        height=110,
    )

    drug_name = st.text_input(
        "Optional: medicine name to look up",
        placeholder="e.g. paracetamol",
    )

    generate = st.button("Generate structured view", type="primary")

    if generate:
        if not concern or not concern.strip():
            st.error("Please enter a health concern first.")
            return

        st.subheader("Structured Response")

        # Section 1
        st.markdown("### 1. Understanding the Concern")
        st.write(concern.strip())

        # Section 2 - basic urgency (will be replaced in later step)
        st.markdown("### 2. Urgency Check (basic)")
        lower = concern.lower()
        high_keywords = ["chest pain", "difficulty breathing", "severe", "unconscious", "bleeding heavily", "stroke", "heart attack", "one side", "sudden weakness"]
        moderate_keywords = ["fever", "pain", "vomit", "dizziness", "bleeding", "swelling", "burning sensation", "blood in"]

        if any(k in lower for k in high_keywords):
            st.error("Possible high urgency signals detected. Seek emergency care immediately if symptoms are serious.")
        elif any(k in lower for k in moderate_keywords):
            st.warning("Moderate concern indicators present. Monitor closely and consider professional medical review if symptoms worsen or persist.")
        else:
            st.info("Based on the description this appears low-to-moderate. Continue to monitor for any change.")

        # Section 3
        st.markdown("### 3. Possible Next Steps / Remedies (general)")
        st.markdown(
            """
- Rest and maintain good hydration  
- Monitor symptoms over the next 24–48 hours  
- For mild symptoms, pharmacy advice on suitable over-the-counter options may help  
- Seek medical attention if symptoms persist, worsen, or new concerning signs appear
            """
        )

        # Section 4 - drug lookup
        if drug_name and drug_name.strip():
            st.markdown("### 4. Drug Information")
            with st.spinner("Looking up drug information..."):
                result = search_drug(drug_name.strip())
            if result:
                st.json(result)
            else:
                st.write("No detailed information returned.")

        # Section 5
        st.markdown("### 5. Notes")
        st.write(
            "This is a basic structured breakdown produced by the current developmental version. "
            "Later versions will include improved urgency logic, explainable risk models, "
            "and richer drug-safety information."
        )

    # Sidebar – samples
    with st.sidebar:
        st.header("Sample Concerns")
        st.caption("Click to inspect (copy into the main box if needed)")
        if samples:
            for i, item in enumerate(samples[:12]):
                concern_text = item.get("concern", "")
                if st.button(concern_text[:55] + ("..." if len(concern_text) > 55 else ""), key=f"s_{i}"):
                    st.session_state["last_sample"] = concern_text
        else:
            st.write("No sample data loaded.")

        if "last_sample" in st.session_state:
            st.info(st.session_state["last_sample"])


if __name__ == "__main__":
    main()
