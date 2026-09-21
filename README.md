# MedFindr

**Current Stage: V-0.7 (Developmental)**

Simple prototype for turning a health concern into structured sections.  
Made this for learning and portfolio building. Not a finished product yet.

Still a lot of things left to improve — better risk scoring, more solid drug interaction handling, cleaner UI, proper testing, etc. This is just the early working version so I can keep adding pieces without rewriting everything later.

## What it does right now

- User types a health concern
- System breaks it into simple sections (understanding, urgency, possible remedies, drug info if mentioned, next steps)
- Basic OpenFDA drug lookup
- Some sample concerns included for testing

## How to run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Important

This is **not medical advice**.  
It is a developmental prototype only. Always consult a real doctor or pharmacist.

## Structure

- `app.py` — main Streamlit interface (kept very simple on purpose)
- `utils/drug_lookup.py` — basic OpenFDA calls
- `data/sample_concerns.json` — list of common concerns + example responses for testing
- `requirements.txt`

More features and refinements will come in later versions.
