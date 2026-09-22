# MedFindr X1.2

MedFindr is a focused med × pharma portfolio prototype built around a simple, auditable workflow: turn a free-text health concern into a structured response, expose the rule-based urgency signals that were matched, optionally surface an explainable-model layer, and retrieve basic drug-label information from OpenFDA.

> Status: X1.2 — consolidated working release

## What X1.2 includes

- Structured response pipeline with separated, testable components
- Transparent rule-based urgency / red-flag layer
- Explainable Boosting Machine integration with a clearly labelled fallback when no trained model is present
- Basic OpenFDA drug-label lookup
- Patient and Staff presentation modes
- Sample concern workflow
- Regression tests for existing urgency behaviour
- Evaluation reporting with confusion matrix and per-class metrics
- Executable evaluation script from the repository root
- Cached EBM model loading
- Explicit prototype/non-clinical boundaries

## Architecture

- app.py — Streamlit presentation layer
- config.py — central configuration and release metadata
- utils/urgency.py — transparent rule-based urgency engine
- utils/ebm_risk.py — optional explainable model layer
- utils/response_engine.py — response orchestration
- utils/drug_lookup.py — OpenFDA label lookup
- data/ — evaluation and sample fixtures
- scripts/evaluate.py — evaluation report
- scripts/train_ebm.py — optional model training workflow
- tests/ — regression and contract tests
- DEVELOPERS_NOTES.md — engineering history and decisions

## Run locally

Install dependencies with: pip install -r requirements.txt

Start the app with: streamlit run app.py

Run regression tests with: python -m unittest discover -s tests -v

Run the evaluation report with: python scripts/evaluate.py

## Design principles

1. Auditable before clever: rule matches and model status are exposed.
2. Small, testable modules: the UI stays thin and the response pipeline is independently testable.
3. Evidence-aware: drug information is retrieved from the configured OpenFDA label endpoint.
4. No clinical overclaiming: software evaluation results are not clinical validation.
5. Portfolio-ready progression: future features can extend the architecture without rewriting the core.

## Current scope and limitations

The urgency engine is a small keyword/rule prototype. The bundled evaluation set is intentionally limited and must not be interpreted as evidence of clinical accuracy. The EBM layer only becomes a trained model when the optional training workflow produces the expected artifact; otherwise the application clearly identifies its fallback behaviour.

## Roadmap

X1.3: stronger evidence/source metadata and improved evaluation coverage.

X2: auditable medication-safety and interaction workflows using explicit datasets, with expanded automated testing.

Future: deployment hardening, richer provenance, broader datasets, model monitoring, and portfolio-grade engineering documentation.

## Portfolio note

This repository is maintained as a student-built portfolio project and should be evaluated as a software prototype rather than a medical product.
