"""MedFindr Streamlit interface over the testable response pipeline."""

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
from utils.response_engine import build_response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@st.cache_data
def load_sample_concerns() -> list[dict[str, Any]]:
    try:
        with SAMPLE_CONCERNS_PATH.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        return data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError) as exc:
        logger.warning("Could not load sample concerns: %s", exc)
        return []


def render_drug_result(result: dict[str, Any]) -> None:
    status = result.get("status")
    if status == "error":
        st.error(result.get("message", "Drug information could not be retrieved."))
        return
    if status == "not_found":
        st.info(result.get("message", "No matching drug label was found."))
        return
    if status != "success":
        st.info(result.get("message", "No drug information was returned."))
        return

    st.markdown("#### Retrieved label information")
    left, right = st.columns(2)
    with left:
        st.markdown(f"**Brand:** {result.get('brand_name', 'N/A')}")
        st.markdown(f"**Generic:** {result.get('generic_name', 'N/A')}")
        st.markdown(f"**Substance:** {result.get('substance_name', 'N/A')}")
    with right:
        st.markdown(f"**Manufacturer:** {result.get('manufacturer', 'N/A')}")
        st.markdown(f"**Route:** {result.get('route', 'N/A')}")
        st.markdown(f"**Product type:** {result.get('product_type', 'N/A')}")

    for key, label in (
        ("boxed_warning_snippet", "Boxed warning"),
        ("warnings_snippet", "Warnings"),
        ("indications_snippet", "Indications / usage"),
        ("dosage_snippet", "Dosage / administration"),
    ):
        if result.get(key):
            st.markdown(f"**{label}**")
            st.write(result[key])

    with st.expander("Source and provenance"):
        st.caption(f"Source: {result.get('source', 'Not specified')}")
        st.caption(f"Source type: {result.get('source_type', 'Not specified')}")
        st.caption(f"Retrieved at (UTC): {result.get('retrieved_at_utc', 'Not specified')}")
        st.caption(f"Query: {result.get('query', 'Not specified')}")


def render_structured_response(response: Any, view_mode: str) -> None:
    for section in response.sections:
        st.markdown(f"### {section.title}")

        if section.level == "high":
            st.error(section.content)
        elif section.level == "moderate":
            st.warning(section.content)
        elif section.level == "low":
            st.info(section.content)
        elif section.level == "error":
            st.error(section.content)
        else:
            st.write(section.content)

        for item in section.items:
            st.markdown(f"- {item}")

    if response.drug_result is not None:
        st.markdown("### 5. Drug Information")
        render_drug_result(response.drug_result)

    if response.errors:
        st.error("Some optional inputs could not be processed:")
        for error in response.errors:
            st.markdown(f"- {error}")

    if view_mode == "staff" and response.ebm is not None:
        with st.expander("Technical detail (Staff)"):
            st.json(response.ebm.to_dict())

    st.markdown("### Scope and provenance")
    st.caption(response.notes)
    st.caption(DISCLAIMER)


def main() -> None:
    st.set_page_config(
        page_title=f"{APP_NAME} {APP_VERSION}",
        page_icon="🧬",
        layout="centered",
    )

    st.title(APP_NAME)
    st.caption(f"{APP_VERSION} • {APP_CAPTION}")
    st.warning(DISCLAIMER)

    view_mode = st.radio(
        "View mode",
        ["Patient", "Staff"],
        horizontal=True,
        help="Staff view exposes additional technical model details.",
    ).lower()

    samples = load_sample_concerns()
    with st.sidebar:
        st.header("Sample concerns")
        st.caption("Use a sample to inspect the prototype workflow.")
        for index, item in enumerate(samples[:12]):
            concern_text = str(item.get("concern", "")).strip()
            if not concern_text:
                continue
            label = concern_text[:55] + ("..." if len(concern_text) > 55 else "")
            if st.button(label, key=f"sample_{index}", use_container_width=True):
                st.session_state["concern_input"] = concern_text
                st.rerun()

    concern_default = st.session_state.get("concern_input", "")
    with st.form("medfindr_form", clear_on_submit=False):
        concern = st.text_area(
            "Health concern",
            value=concern_default,
            max_chars=2000,
            height=120,
            placeholder="Example: mild headache and body ache for two days",
            help="Describe the concern in plain language. This prototype does not diagnose conditions.",
        )
        drug_name = st.text_input(
            "Optional drug name",
            max_chars=120,
            placeholder="Example: paracetamol",
            help="Retrieves label information from OpenFDA; it does not recommend a medication.",
        )
        submitted = st.form_submit_button(
            "Generate structured view",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        if not concern.strip():
            st.error("Please enter a health concern first.")
            return

        with st.spinner("Processing the structured workflow..."):
            try:
                response = build_response(
                    concern=concern,
                    drug_name=drug_name,
                )
            except Exception:
                logger.exception("Unexpected error in response pipeline")
                st.error(
                    "MedFindr could not complete this request. "
                    "Please try again with a shorter description."
                )
                return

        st.session_state["concern_input"] = concern
        st.subheader("Structured response")
        render_structured_response(response, view_mode=view_mode)


if __name__ == "__main__":
    main()
