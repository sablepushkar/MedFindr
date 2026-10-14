# MedFindr — X2

**Med × Pharma × Data × Technology**

MedFindr is my student-built healthcare/pharmaceutical information prototype. It combines a small, transparent rule-based concern flagger with public drug-label lookup and a repeatable evaluation workflow. The purpose is to make results inspectable and rule checks reproducible—not to claim a medical product.

## What currently works

- Streamlit interface for a bounded free-text concern and optional medicine name.
- Explainable rule-based flags, with overlapping moderate phrases prevented from inflating the same score.
- Optional local model output kept separate from rule results, with fallback behaviour labelled.
- Public OpenFDA drug-label lookup with source and retrieval metadata.
- Structured evidence records that keep generated rules distinct from retrieved label information.
- A labelled local fixture and evaluation scripts that report mismatches and software-behaviour metrics.
- Signal evaluation JSON reports with fixture SHA-256 fingerprint and source revision.
- Human-review fields and JSON export for a session-scoped review workflow.
- Regression tests for the rule engine, evaluation inputs, external lookup failure states, and Streamlit review flow.

## Main workflow

~~~text
Concern / optional medicine name
        ↓
Input validation
        ↓
Rule-based information flags ── optional model/fallback shown separately
        ↓
Public label lookup (when requested)
        ↓
Structured result + evidence/source notes
        ↓
Synthetic evaluation fixture + reproducible report
        ↓
Optional human review and JSON export
~~~

The app is a single Streamlit/Python application. It does not currently include user accounts, a patient database, a separate backend service, or persistent patient records.

## Run locally

~~~bash
python -m pip install -r requirements.txt
streamlit run app.py
~~~

Run the tests and evaluations:

~~~bash
python -m unittest discover -s tests -v
python scripts/evaluate.py
python scripts/evaluate_signals.py
python scripts/evaluate_signals.py --json-out reports/signal-evaluation.json
python scripts/evaluate_reviews.py
~~~

The signal JSON report includes the fixture filename and SHA-256 fingerprint, the GitHub Actions source revision when available, aggregate status counts, agreement, and case-level mismatches. Generated reports should be reviewed before sharing and are not committed by default.

## Data and safety boundaries

- The evaluation and sample data are development fixtures, not clinical datasets.
- The rule engine is not a validated triage tool and its output is not a diagnosis.
- Evaluation agreement measures matching against a small manually labelled fixture only; it is not a measure of medical safety or real-world effectiveness.
- OpenFDA results are public label information, not a recommendation to start, stop, or change medication.
- Retrieval failures are shown as errors; they must not be interpreted as proof that a medicine or label does not exist.
- Do not enter real patient-identifying information.

## Current limitations

The rule set and evaluation fixtures are small; labels are manually assigned; external retrieval depends on source availability; and no authentication, patient database, institutional integration, or production deployment is implemented. Review records are session-scoped, not a governed review database or compliance audit log. Provenance improves inspectability but does not establish clinical validity.

See DEVELOPERS_NOTES.md, docs/evaluation.md, and docs/evidence-reliability.md for implementation and scope details.
