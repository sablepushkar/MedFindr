"""
MedFindr - Main application entry point
Version: 09.0
"""

from __future__ import annotations

import json
import logging
from typing import Any

import streamlit as st

from config import APP_CAPTION, APP_NAME, APP_VERSION, DISCLAIMER, SAMPLE_CONCERNS_PATH
from utils.response_engine import build_response

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


def render_structured_response(response) -> None:
    for section in response.sections:
        st.markdown(f"### {section.title}")

        if section.level == "high":
            st.error(section.content)
        elif section.level == "moderate":
            st.warning(section.content)
        elif section.level == "low":
            st.info(section.content)
        else:
            st.write(section.content)

        for item in section.items:
            st.markdown(f"- {item}")

    if response.drug_result:
        st.markdown("### 5. Drug Information")
        render_drug_result(response.drug_result)

    st.markdown("### Notes")
    st.write(response.notes)


def main() -> None:
    st.set_page_config(page_title=f"{APP_NAME} {APP_VERSION}", page_icon="🩺", layout="centered")

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

    if st.button("Generate structured view", type="primary"):
        if not concern or not concern.strip():
            st.error("Please enter a health concern first.")
            return

        with st.spinner("Generating structured response..."):
            response = build_response(concern=concern, drug_name=drug_name)

        st.subheader("Structured Response")
        render_structured_response(response)

    with st.sidebar:
        st.header("Sample Concerns")
        st.caption("Click to inspect")
        if samples:
            for i, item in enumerate(samples[:12]):
                text = item.get("concern", "")
                label = text[:55] + ("..." if len(text) > 55 else "")
                if st.button(label, key=f"sample_{i}"):
                    st.session_state["last_sample"] = text
        else:
            st.write("No sample data loaded.")

        if "last_sample" in st.session_state:
            st.info(st.session_state["last_sample"])


if __name__ == "__main__":
    main()
