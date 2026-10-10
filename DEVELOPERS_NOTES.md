# MedFindr — Developer Notes

## VERSION X1 — rule reliability and portfolio cleanup

I kept the current Streamlit → response-engine architecture. It is small enough to understand end to end, and there is no reason to add a database or service layer just to make the project look bigger.

### Work in this update

- Review the rule-scoring behavior where a specific phrase also contains a general phrase (for example, `high fever` contains `fever`).
- Count a matched concept once when a longer, more specific phrase already represents it.
- Add regression tests for those overlaps so the score does not rise just because the wording is more specific.
- Re-state the actual runtime and data boundaries in the README.

### Existing flow retained

`app.py` collects the input and renders the response. `utils/validation.py` bounds input. `utils/response_engine.py` orchestrates the modules. `utils/urgency.py` contains the transparent rule layer. `utils/drug_lookup.py` handles public label retrieval and provenance. The optional EBM path remains explicitly optional.

### Verification to run before promotion

```bash
python -m unittest discover -s tests -v
python scripts/evaluate.py
python -m compileall -q .
```

Do not mark the update as tested until those commands and the GitHub Actions workflow have actually completed successfully.

### Not part of X1

No clinical claims, patient accounts, patient-record database, authentication, real hospital integration, or production triage capability is being added. Synthetic fixtures remain software tests only.
