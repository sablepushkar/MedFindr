# Checking MedFindr's rules

I use small labelled examples to catch changes in rule behaviour. The examples are not a clinical dataset.

## Run the checks

~~~bash
python scripts/evaluate.py
python scripts/evaluate.py --json-out reports/medfindr-evaluation.json
python scripts/evaluate_signals.py
python scripts/evaluate_signals.py --json-out reports/signal-evaluation.json
python scripts/evaluate_reviews.py
~~~

The signal evaluator checks the fixture format before running. Its report includes the number of cases, agreement with the expected labels, output counts and the cases that did not match. It also records a SHA-256 hash of the fixture and, in GitHub Actions, the source revision.

## How to read the result

- Agreement is the share of examples where the output matches the label in the fixture.
- A mismatch is a case worth reviewing; it does not automatically mean the rule is wrong or the label is right.
- The fixture hash identifies the exact file contents, not the quality of the labels.
- Results should only be compared carefully when the fixture and code version are known.

These checks are useful for software regressions. They do not establish clinical accuracy, patient safety or real-world effectiveness.
