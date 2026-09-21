"""
MedFindr - Main application entry point.
Version: 07.2

Interface remains minimal. Drug lookup now returns richer structured data.
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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_sample_concerns() -> list[dict[str, Any]]:
    try:
        with open(SAMPLE_CONCERNS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception as exc:
        logger.warning("Could not load sample concerns: %s", exc)
        return []


def render_drug_result(result: dict[str, Any]) -> None:
    """Render drug lookup result in a clean, readable way."""
    status = result.get("status")

    if status == "error":
        st.error(result.get("message", "Unknown error"))
        return

    if status == "not_found":
        st.warning(result.get("message", "No information found"))
        return

    # Success case
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Brand name:** {result.get('brand_name', 'N/A')}")
        st.markdown(f"**Generic name:** {result.get('generic_name', 'N/A')}")
        st.markdown(f"**Substance:** {result.get('substance_name', 'N/A')}")
    with col2:
        st.markdown(f"**Manufacturer:** {result.get('manufacturer', 'N/A')}")
        st.markdown(f"**Route:** {result.get('route', 'N/A')}")
        st.markdown(f"**Product type:** {result.get('product_type', 'N/A')}")

    if result.get("boxed_warning_snippet"):
        st.error("**Boxed Warning (excerpt)**")
        st.write(result["boxed_warning_snippet"])

    if result.get("warnings_snippet"):
        st.warning("**Warnings (excerpt)**")
        st.write(result["warnings_snippet"])

    if result.get("indications_snippet"):
        st.info("**Indications (excerpt)**")
        st.write(result["indications_snippet"])

    if result.get("dosage_snippet"):
        st.markdown("**Dosage & Administration (excerpt)**")
        st.write(result["dosage_snippet"])


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

    concern = st.text_area(
        "Describe the health concern",
        placeholder="Example: mild headache and body ache for 2 days",
        height=110,
    )

    drug_name = st.text_input(
        "Optional: medicine name to look up",
        placeholder="e.g. paracetamol / ibuprofen / amoxicillin",
    )

    generate = st.button("Generate structured view", type="primary")

    if generate:
        if not concern or not concern.strip():
            st.error("Please enter a health concern first.")
            return

        st.subheader("Structured Response")

        st.markdown("### 1. Understanding the Concern")
        st.write(concern.strip())

        st.markdown("### 2. Urgency Check (basic)")
        lower = concern.lower()
        high_keywords = [
            "chest pain", "difficulty breathing", "severe", "unconscious",
            "bleeding heavily", "stroke", "heart attack", "one side",
            "sudden weakness", "severe headache with fever"
        ]
        moderate_keywords = [
            "fever", "pain", "vomit", "dizziness", "bleeding",
            "swelling", "burning sensation", "blood in"
        ]

        if any(k in lower for k in high_keywords):
            st.error("Possible high urgency signals detected. Seek emergency care immediately if symptoms are serious.")
        elif any(k in lower for k in moderate_keywords):
            st.warning("Moderate concern indicators present. Monitor closely and consider professional medical review if symptoms worsen or persist.")
        else:
            st.info("Based on the description this appears low-to-moderate. Continue to monitor for any change.")

        st.markdown("### 3. Possible Next Steps / Remedies (general)")
        st.markdown(
            """
- Rest and maintain good hydration  
- Monitor symptoms over the next 24–48 hours  
- For mild symptoms, pharmacy advice on suitable over-the-counter options may help  
- Seek medical attention if symptoms persist, worsen, or new concerning signs appear
            """
        )

        if drug_name and drug_name.strip():
            st.markdown("### 4. Drug Information")
            with st.spinner("Looking up drug information..."):
                result = search_drug(drug_name.strip())
            render_drug_result(result)

        st.markdown("### 5. Notes")
        st.write(
            "This is a developmental structured breakdown. "
            "Later versions will include improved urgency logic, explainable risk models, "
            "and richer drug-safety information."
        )

    with st.sidebar:
        st.header("Sample Concerns")
        st.caption("Click to inspect")
        if samples:
            for i, item in enumerate(samples[:12]):
                concern_text = item.get("concern", "")
                if st.button(
                    concern_text[:55] + ("..." if len(concern_text) > 55 else ""),
                    key=f"s_{i}",
                ):
                    st.session_state["last_sample"] = concern_text
        else:
            st.write("No sample data loaded.")

        if "last_sample" in st.session_state:
            st.info(st.session_state["last_sample"])


if __name__ == "__main__":
    main()
