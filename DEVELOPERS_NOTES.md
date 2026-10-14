# MedFindr — Developer Notes

## X2 — reproducible rule evaluation

I kept the existing Streamlit flow and rule engine in place for this update. The most useful next step was making it easier to tell whether a rule change broke something, rather than adding another broad feature.

### What changed

- Added strict checks for evaluation case shape, non-empty concern text, known labels, and unique case IDs.
- Added a report builder with overall agreement, confusion matrix, and per-class precision/recall/support.
- Added `--json-out` so an evaluation run can be saved and compared later.
- Added regression tests for the report and malformed evaluation fixtures.
- Kept the report explicit that a small labelled fixture is not clinical validation.

### How I check it

```bash
python -m unittest discover -s tests -v
python scripts/evaluate.py
python scripts/evaluate.py --json-out reports/medfindr-evaluation.json
```

### What I have not claimed

This does not make the rule engine medically validated. The sample set is small and manually labelled. The application is still a prototype; no patient database, account system, or production deployment was added.

### Next things worth doing

The next useful work is expanding the evaluation cases with deliberately tricky examples, reviewing false positives and false negatives, and making external-source failure states easier to inspect. I would not add more model complexity until those checks are better.


## SignalGraph and review workflow

- `utils/clinical_data.py` performs bounded phrase matching and skips common direct negations; it does not infer a diagnosis.
- `utils/safety_signals.py` flags only configured medication/context patterns and explicitly avoids causality claims.
- `utils/evidence.py` records whether an item came from a prototype rule or an external label lookup.
- `utils/analysis_trace.py` is an in-memory debugging trace, not an audit log.
- `utils/review.py` validates session-scoped review fields; `utils/review_export.py` serializes a JSON bundle on request. There is no review database or persistence guarantee.
- Run `python scripts/evaluate_signals.py` and `python scripts/evaluate_reviews.py` to exercise the included synthetic fixtures.
