# MedFindr — VERSION X1

**Med × Pharma × Data × Technology**

MedFindr is my student-built healthcare/pharmaceutical technology prototype for turning a short concern into a structured, traceable information view. The point is not to claim a diagnosis; it is to make the software workflow understandable, testable, and honest about its limits.

## What it does today

- Accepts a bounded free-text concern through a Streamlit interface.
- Runs a transparent, rule-based informational flag layer.
- Keeps the optional Explainable Boosting Machine output separate from the rule result and labels the fallback when a compatible model is unavailable.
- Can retrieve public drug-label information from OpenFDA, with source and retrieval metadata.
- Displays sample concerns, structured sections, and a technical staff view.
- Includes regression tests and a small rule-engine evaluation script.

## Workflow

```text
Concern + optional drug name
        ↓
Input validation
        ↓
Response engine ──→ prototype flagging
        │            optional model/fallback
        └──────────→ OpenFDA label lookup
        ↓
Structured result with source notes
```

The app is a single Streamlit/Python application. It does not currently include user accounts, a patient database, a separate backend service, or persistent patient records.

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Run checks:

```bash
python -m unittest discover -s tests -v
python scripts/evaluate.py
```

## Why this update is VERSION X1

This update focuses on correctness at the edges rather than adding a big feature list. In particular, overlapping rule phrases such as `fever` and `high fever` or `vomiting` and `persistent vomiting` should not inflate the prototype score for the same underlying signal. The regression suite should lock that behavior down so later rule changes remain deliberate.

## Data and safety boundaries

- The bundled evaluation and sample data are development fixtures, not clinical datasets.
- The rule engine is not a validated triage tool and its output is not a diagnosis.
- Model output is only available when a compatible local model artifact exists; synthetic training is not clinical evidence.
- OpenFDA results are retrieved public label information, not a recommendation to start, stop, or change medication.
- Do not enter real patient-identifying information.

## Current limitations

The rule layer is intentionally small; the evaluation set is small; external retrieval depends on source availability; and no authentication, database, institutional integration, or production deployment is implemented. These are explicit boundaries, not hidden capabilities.

## Next practical steps

1. Expand tests for overlapping rules, input boundaries, and external-source failures.
2. Add a repeatable evaluation report with per-class counts and known failure cases.
3. Improve provenance and result export without collecting patient records.
4. Only consider larger data/model work after the evaluation and privacy story is clear.

See [DEVELOPERS_NOTES.md](DEVELOPERS_NOTES.md) for the audit notes and this update's scope.
