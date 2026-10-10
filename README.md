# MedFindr — X2

**Med × Pharma × Data × Technology**

MedFindr is my student-built healthcare/pharmaceutical information prototype. It combines a small, transparent rule-based concern flagger with public drug-label lookup and a repeatable evaluation workflow. The purpose of this update is to make the results easier to inspect and the rule checks easier to reproduce—not to claim a medical product.

## What currently works

- Streamlit interface for a bounded free-text concern and optional medicine name.
- Explainable rule-based flags, with overlapping moderate phrases prevented from inflating the same score.
- Optional local model output kept separate from rule results, with fallback behaviour labelled.
- Public OpenFDA drug-label lookup with source and retrieval metadata.
- A labelled local fixture and evaluation script that reports a confusion matrix, per-class precision/recall, and individual mismatches.
- Optional JSON report output for comparing runs and preserving review evidence.
- Regression tests for the rule engine and evaluation inputs.

## Main workflow

```text
Concern / optional medicine name
        ↓
Input validation
        ↓
Rule-based information flags ── optional model/fallback shown separately
        ↓
Public label lookup (when requested)
        ↓
Structured result + source notes
        ↓
Offline evaluation fixture for rule regressions
```

The app is a single Streamlit/Python application. It does not currently include user accounts, a patient database, a separate backend service, or persistent patient records.

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Run the tests and evaluation:

```bash
python -m unittest discover -s tests -v
python scripts/evaluate.py
python scripts/evaluate.py --json-out reports/medfindr-evaluation.json
```

The JSON report contains the fixture version, total and matched cases, accuracy, confusion matrix, per-class metrics, and case-level outcomes. The output file is generated locally and should be reviewed before sharing.

## X2 focus

X2 makes the evaluation workflow more useful for ongoing development. The evaluator now rejects malformed cases, unknown labels, blank concerns, and duplicate case IDs rather than silently allowing a broken fixture to distort the report. It can write a machine-readable report so future changes can be compared using the same labelled cases.

## Data and safety boundaries

- The evaluation and sample data are development fixtures, not clinical datasets.
- The rule engine is not a validated triage tool and its output is not a diagnosis.
- Evaluation accuracy measures agreement with this small hand-labelled fixture only; it is not a measure of medical safety or real-world effectiveness.
- OpenFDA results are public label information, not a recommendation to start, stop, or change medication.
- Do not enter real patient-identifying information.

## Current limitations

The rule set and evaluation fixture are small; labels are manually assigned; external retrieval depends on source availability; and no authentication, patient database, institutional integration, or production deployment is implemented. The report is useful for regression checks but cannot establish clinical validity.

## Next practical steps

1. Add more adversarial rule examples and review false positives/negatives deliberately.
2. Track source freshness and external lookup failures as explicit states.
3. Improve provenance and result export without collecting patient records.
4. Only consider larger data/model work after evaluation quality and privacy boundaries are clear.

See [DEVELOPERS_NOTES.md](DEVELOPERS_NOTES.md) and [docs/evaluation.md](docs/evaluation.md) for the update details.
