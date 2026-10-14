# MedFindr evaluation workflow

The fixture in data/evaluation_set.json is a small set of manually labelled examples used to catch regressions in the rule-based urgency layer. The signal fixture in data/signal_evaluation_set.json exercises a separate medication-signal prototype.

## Run

~~~bash
python scripts/evaluate.py
python scripts/evaluate.py --json-out reports/medfindr-evaluation.json
python scripts/evaluate_signals.py
python scripts/evaluate_signals.py --json-out reports/signal-evaluation.json
python scripts/evaluate_reviews.py
~~~

The signal evaluator validates case structure, non-empty concerns, unique IDs, and allowed expected statuses before running. Its JSON report includes the fixture's SHA-256 fingerprint, the source revision when running in GitHub Actions, aggregate status counts, agreement, and each mismatch. This makes it easier to compare results without losing which fixture bytes were evaluated.

## Interpreting the numbers

- **Agreement** is the percentage of fixture labels matched by the current rule output.
- **Status counts** describe the output distribution for this fixture.
- **Mismatches** are cases to inspect; a mismatch does not prove that either the rule or the manual label is clinically correct.
- The fixture hash identifies the exact input file bytes, not the quality or representativeness of the labels.
- A source revision helps identify the code revision used in CI; local runs without GitHub Actions are marked local-unpinned.

These are software regression checks on small, manually labelled fixtures. They are not representative clinical datasets, clinical validation, a safety study, or evidence that MedFindr can triage real people. Keep generated reports out of commits unless the exact fixture and review context are intentionally documented.
