# MedFindr

MedFindr is a project I have been building to explore the overlap between healthcare information, pharmacy data and Python. It is a small Streamlit app, not a medical product. I wanted to see how simple rules and information from a public drug-label source could work together, and how tests can help catch mistakes when I change the code.

## What it does

- Takes a short text concern and an optional medicine name.
- Runs a small rule-based check and shows an informational flag.
- Can look up public drug-label information through OpenFDA.
- Keeps rule-generated output separate from data returned by the external source.
- Shows source details and lookup status.
- Includes small labelled examples for checking rule behaviour.
- Can export a review from the current session as JSON.
- Has tests for rule logic, evaluation inputs, lookup failures and parts of the Streamlit review flow.

## How it works

~~~text
Text entered by user
        ↓
Input checks
        ↓
Rule-based flag ── optional model output shown separately
        ↓
Optional public drug-label lookup
        ↓
Result with source notes
        ↓
Local evaluation and optional review export
~~~

The app is currently one Python/Streamlit application. It does not have a separate backend, user accounts or a database of patient records.

## Run it

~~~bash
python -m pip install -r requirements.txt
streamlit run app.py
~~~

To run the tests and included checks:

~~~bash
python -m unittest discover -s tests -v
python scripts/evaluate.py
python scripts/evaluate_signals.py
python scripts/evaluate_signals.py --json-out reports/signal-evaluation.json
python scripts/evaluate_reviews.py
~~~

The evaluation report shows agreement with the labels in the small fixture, cases that did not match and a SHA-256 fingerprint of the input file. The fingerprint helps identify which fixture was used; it does not tell us whether the labels are medically correct.

## What I am careful not to claim

- The rules are not clinically validated and cannot diagnose or triage a person.
- The example cases are small development fixtures, not a clinical dataset.
- A successful OpenFDA lookup only means the source returned data. It is not personal medical advice.
- A failed lookup does not prove that a medicine or label does not exist.
- Review exports are session-based and are not a formal audit record.
- Do not enter real patient-identifying information or use this app to make medication decisions.

I am keeping the project focused on readable code, traceable sources and tests before adding more features. See DEVELOPERS_NOTES.md and ARCHITECTURE.md for more detail.
