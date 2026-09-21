import streamlit as st
import json
from utils.drug_lookup import search_drug

st.set_page_config(page_title="MedFindr V-0.7", page_icon="🩺", layout="centered")

st.title("MedFindr")
st.caption("V-0.7 · Developmental prototype · Not medical advice")

st.warning(
    "This is an early developmental version. "
    "It is not a substitute for professional medical advice, diagnosis, or treatment. "
    "Always consult a qualified healthcare provider."
)

# Load sample concerns for testing
try:
    with open("data/sample_concerns.json", "r", encoding="utf-8") as f:
        samples = json.load(f)
except Exception:
    samples = []

# Simple input
concern = st.text_area(
    "Describe the health concern",
    placeholder="Example: mild headache and body ache for 2 days",
    height=100
)

# Optional drug search
drug_name = st.text_input("Optional: enter a medicine name to look up", placeholder="e.g. paracetamol")

if st.button("Generate structured view", type="primary"):
    if not concern.strip():
        st.error("Please enter a concern first.")
    else:
        st.subheader("Structured Response")

        # Section 1
        st.markdown("### 1. Understanding the Concern")
        st.write(concern.strip())

        # Section 2 - very basic urgency placeholder
        st.markdown("### 2. Urgency Check (basic)")
        lower = concern.lower()
        if any(word in lower for word in ["chest pain", "difficulty breathing", "severe", "unconscious", "bleeding heavily"]):
            st.error("Possible high urgency. Please seek emergency care immediately.")
        elif any(word in lower for word in ["fever", "pain", "vomit", "dizziness"]):
            st.warning("Moderate concern. Monitor closely and consider seeing a doctor if it worsens.")
        else:
            st.info("Appears low-moderate based on the description. Still watch for any worsening.")

        # Section 3
        st.markdown("### 3. Possible Next Steps / Remedies (general)")
        st.write(
            "- Rest and stay hydrated\n"
            "- Monitor symptoms for the next 24-48 hours\n"
            "- Over-the-counter options may help for mild cases (check with pharmacist)\n"
            "- See a doctor if symptoms persist or get worse"
        )

        # Section 4 - drug lookup if provided
        if drug_name.strip():
            st.markdown("### 4. Drug Information")
            result = search_drug(drug_name.strip())
            if result:
                st.json(result)
            else:
                st.write("No detailed information found or API issue.")

        # Section 5
        st.markdown("### 5. Notes")
        st.write(
            "This is a very basic structured breakdown for testing. "
            "Later versions will have better risk models, proper interaction checks, "
            "and more refined sections."
        )

# Sidebar with samples
with st.sidebar:
    st.header("Sample Concerns (for testing)")
    if samples:
        for i, item in enumerate(samples[:15]):  # show first 15
            if st.button(item["concern"][:60] + "...", key=f"sample_{i}"):
                st.session_state["prefill"] = item["concern"]
                st.rerun()
    else:
        st.write("Sample data not loaded.")

if "prefill" in st.session_state:
    # simple way to prefill - user can copy or we can improve later
    st.info(f"Sample selected: {st.session_state['prefill']}")
