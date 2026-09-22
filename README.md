# MedFindr

**MedFindr v2.0 — student-built healthcare/pharma technology prototype for structured information, transparent signals, evidence provenance, human review, and workflow-oriented experimentation.**

MedFindr is a portfolio-scale Python/Streamlit project exploring how unstructured health-concern text can be transformed into structured information, prototype medication-related safety signals, evidence objects, and a human review workflow.

> **Scope:** MedFindr is an information-engineering prototype. It is not a diagnostic system, clinical decision-support product, pharmacovigilance validation system, medical-advice service, or compliance audit platform.

## v2 workflow
`Input → Validation → Structured information → Data quality → Signal → Evidence → Human review → Disposition → Export`

### v2 capabilities
- normalized clinical/medication representation
- explicit input completeness and missing information
- prototype medication-related safety signals
- explainable risk layer
- evidence and source provenance
- human-in-the-loop Review Workspace
- reviewer reasoning, evidence reviewed, follow-up notes, and disposition
- session-scoped review state
- portable JSON review bundle
- synthetic evaluation fixtures
- regression tests and CI

## Human workflow
1. **Input** — plain-language concern and optional public-label lookup term.
2. **Validation** — bounded and normalized input.
3. **Structure** — symptom, medication, timing, and context extraction.
4. **Data quality** — available and missing information are made explicit.
5. **Signals** — deterministic prototype rules identify software-level patterns.
6. **Evidence** — rule evidence and optional retrieved public label evidence carry provenance.
7. **Review** — a human records what was checked, reasoning, missing information, follow-up, and disposition.
8. **Export** — the current analysis and review state can be exported as JSON.

The review layer is deliberately session-scoped. MedFindr does not add an application database, patient account system, or hidden persistence in v2.

## Architecture
`USER → STREAMLIT UI → VALIDATION → STRUCTURED CLINICAL INFORMATION → DATA QUALITY → URGENCY + SAFETY SIGNALS → EXPLAINABLE RISK → EVIDENCE / OPENFDA → HUMAN REVIEW WORKSPACE → DISPOSITION + JSON EXPORT`

## Evaluation
Synthetic fixtures cover urgency, SignalGraph behavior, and v2 review workflow behavior. These are software engineering checks, not clinical validation. Run `python scripts/evaluate_reviews.py` for the v2 review fixture set.

## Security and data boundary
- no application database
- no patient account system
- no patient identifier field
- no secrets committed to source
- bounded text inputs
- external retrieval separated from generated analysis
- review state is session-scoped
- export is explicit user action
- UI errors are generic while unexpected exceptions are logged server-side

A real deployment would require authentication, authorization, secure persistence, retention rules, encryption, privacy review, audit controls, and regulatory analysis.

## Run locally
```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/evaluate.py
python scripts/evaluate_signals.py
python scripts/evaluate_reviews.py
streamlit run app.py
```

## Project direction
MedFindr is a student-built project created and directed by Pushkar Sable. External assistance may be used selectively for research, implementation support, debugging, and review; product direction and final acceptance remain with the project creator.

## Future directions
Richer terminology normalization, literature/evidence adapters, validated pharmacovigilance datasets, model benchmarking, institutional API adapters, device/event adapters, role-based access controls, secure persistence, privacy-preserving analytics, and deployment architecture are possible next stages. Any clinical or regulated use would require domain validation and governance beyond this repository.
