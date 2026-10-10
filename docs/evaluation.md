# MedFindr evaluation workflow

The evaluation fixture in `data/evaluation_set.json` is a small set of manually labelled examples used to catch regressions in the rule-based urgency layer.

## Run

```bash
python scripts/evaluate.py
python scripts/evaluate.py --json-out reports/medfindr-evaluation.json
```

The terminal output is for quick review. The optional JSON report preserves the fixture version, aggregate agreement, confusion matrix, per-class precision/recall/support, and case-level outcomes.

## Interpreting the numbers

- **Agreement / accuracy** is the percentage of fixture labels matched by the current rule output.
- **Precision** and **recall** are calculated per fixture label from the confusion matrix.
- **Support** is the number of cases carrying that expected label.
- A mismatch is a case to inspect, not proof that either the rule or label is clinically correct.

This is a software regression check on a small, manually labelled fixture. It is not a representative clinical dataset, clinical validation, a safety study, or evidence that MedFindr can triage real people. Keep generated reports out of commits unless they are intentionally reviewed and the exact fixture version is stated.
