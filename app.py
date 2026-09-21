"""
MedFindr - Main application entry point.
Version: 07.3 major

Urgency logic is now fully isolated in utils/urgency.py.
Interface only renders the structured result.
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
from utils.urgency import assess_urgency

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
    status = result.get("status")

    if status == "error":
        st.error(result.get("message", "Unknown error"))
        return

    if status == "not_found":
        st.warning(result.get("message", "No information found"))
        return

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


def render_urgency(result) -> None:
    """Render urgency result with clear visual hierarchy."""
    level = result.level

    if level == "high":
        st.error(f"**Urgency level: HIGH**")
    elif level == "moderate":
        st.warning(f"**Urgency level: MODERATE**")
    else:
        st.info(f"**Urgency level: LOW**")

    st.markdown(result.recommendation)

    if result.reasons:
        st.markdown("**Reasons detected:**")
        for reason in result.reasons:
            st.markdown(f"- {reason}")


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

        # 1. Understanding
        st.markdown("### 1. Understanding the Concern")
        st.write(concern.strip())

        # 2. Urgency (new clean engine)
        st.markdown("### 2. Urgency Assessment")
        urgency_result = assess_urgency(concern)
        render_urgency(urgency_result)

        # 3. Next steps
        st.markdown("### 3. Possible Next Steps / Remedies (general)")
        st.markdown(
            """
- Rest and maintain good hydration  
- Monitor symptoms over the next 24–48 hours  
- For mild symptoms, pharmacy advice on suitable over-the-counter options may help  
- Seek medical attention if symptoms persist, worsen, or new concerning signs appear
            """
        )

        # 4. Drug info
        if drug_name and drug_name.strip():
            st.markdown("### 4. Drug Information")
            with st.spinner("Looking up drug information..."):
                result = search_drug(drug_name.strip())
            render_drug_result(result)

        # 5. Notes
        st.markdown("### 5. Notes")
        st.write(
            "Urgency assessment is currently rule-based and fully transparent. "
            "Later versions will add explainable machine learning models while keeping the same clear output format."
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
