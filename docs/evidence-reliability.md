# Evidence and reliability checks

MedFindr keeps generated rule flags separate from retrieved public drug-label data. Each retrieved evidence record carries the query, retrieval timestamp, source type, and retrieval outcome. A successful lookup means the external service returned a record; it does not mean the label is current for every jurisdiction or that the information is suitable for an individual patient.

## Reproduce the synthetic signal evaluation

~~~bash
python scripts/evaluate_signals.py
python scripts/evaluate_signals.py --json-out reports/signal-evaluation.json
python -m unittest discover -s tests -v
~~~

The JSON report records the evaluation fixture's SHA-256 fingerprint, source revision (GitHub Actions commit SHA when available), case count, agreement, status counts, and case-level mismatches. The same fixture bytes produce the same fingerprint. A report is comparable only when the fixture fingerprint and evaluation logic are considered together.

## What the checks do and do not establish

- Tests cover bounded request handling, malformed external responses, missing results, timestamps, and the synthetic rule-evaluation fixture.
- An external lookup failure is an explicit status, not evidence that a medicine or label does not exist.
- The included fixtures are small, synthetic or manually labelled software tests. Agreement is not clinical accuracy.
- Provenance fields help a reviewer inspect where information came from; they are not a regulated audit trail.
- Do not enter patient-identifying information. Do not use MedFindr to diagnose, triage, or make medication decisions.
