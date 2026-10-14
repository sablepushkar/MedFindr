# MedFindr: portfolio demo

This guide is a short route through the parts of MedFindr that can be checked from the repository. Use synthetic example text only.

## 1. Install and launch

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Open the local Streamlit address printed in the terminal. Enter a non-identifying example concern and, if useful, a medicine name. Do not use personal health information.

## 2. Walk through one result

1. Show the input and the validation step.
2. Point out which output comes from local rules.
3. If an external lookup is attempted, show its status and source details separately.
4. Explain that missing external data is a lookup outcome, not proof that a label does not exist.
5. If using the review export, show that it is a current-session JSON export.

## 3. Run the repeatable checks

```bash
python -m unittest discover -s tests -v
python scripts/evaluate.py
python scripts/evaluate_signals.py
python scripts/evaluate_reviews.py
```

Keep the actual terminal output with the commit used for the demo. Do not report a metric unless it appears in that output, and do not present agreement with the small fixture as clinical validation.

## What this demo establishes

It can demonstrate the local application flow, rule behaviour against included examples, handling of some lookup failures and test coverage. It does not establish diagnostic accuracy, safety for patient use, or clinical validity.
