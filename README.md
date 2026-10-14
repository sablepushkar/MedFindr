# MedFindr

[![Tests](https://github.com/sablepushkar/MedFindr/actions/workflows/medfindr.yml/badge.svg?branch=main)](https://github.com/sablepushkar/MedFindr/actions/workflows/medfindr.yml)

MedFindr is a project I have been building to explore the overlap between healthcare information, pharmacy data and Python. It is a small Streamlit application, not a medical product. I wanted to see how readable rules and information from a public drug-label source could work together, and how tests can catch mistakes as the code changes.

## What it does

- Accepts a short text concern and an optional medicine name.
- Runs a rule-based check and shows an informational flag.
- Can look up public drug-label information through OpenFDA.
- Keeps rule-generated output separate from information returned by the external source.
- Shows source details and lookup status.
- Includes small labelled fixtures for checking rule behaviour.
- Exports a review from the current session as JSON.
- Includes tests for rule logic, evaluation inputs, lookup failures and parts of the review flow.

## Workflow

```text
Text entered
    ↓
Input validation
    ↓
Rule-based flag ── optional model output kept separate
    ↓
Optional OpenFDA label lookup
    ↓
Result with evidence/source notes
    ↓
Evaluation checks or session review export
```

The app is one Python/Streamlit application. It does not have user accounts or a patient-record database.

## Run it

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

In another terminal, run the checks: 

```bash
python -m unittest discover -s tests -v
python scripts/evaluate.py
python scripts/evaluate_signals.py
python scripts/evaluate_reviews.py
```

For a walkthrough of what to run and what evidence to capture, see [the portfolio demo guide](docs/portfolio-demo.md). Evaluation output reports agreement with the small included fixture, mismatches and an input-file fingerprint. That fingerprint identifies the fixture; it does not validate the medical correctness of its labels.

## Limits I want to keep clear

- The rules are not clinically validated and cannot diagnose or triage a person.
- Included examples are small development fixtures, not a clinical dataset.
- A successful OpenFDA lookup means the source returned data; it is not personal medical advice.
- A failed lookup does not prove a medicine or label does not exist.
- Review exports are session-based, not a formal audit record.
- Do not enter real patient-identifying information or use the app to make medication decisions.

I am keeping the project focused on readable code, traceable sources and repeatable checks before adding more features. See [architecture](ARCHITECTURE.md), [evaluation notes](docs/evaluation.md) and [developer notes](DEVELOPERS_NOTES.md).
