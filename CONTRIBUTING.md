# Contributing to MedFindr

MedFindr is a **student-led portfolio project**. Contributions and review are welcome when they preserve the project's engineering and healthcare-safety boundaries.

## Before changing code

Read `README.md`, `ARCHITECTURE.md`, `DEVELOPERS_NOTES.md`, `SECURITY.md`, and `docs/signalgraph-scope.md`.

## Development rules

### 1. Keep the medical boundary explicit

Do not turn prototype signals into claims of diagnosis, causality, treatment recommendation, clinical alerting, or clinical validation.

### 2. Use synthetic/non-sensitive data

Never add real patient information to code, fixtures, screenshots, issues, or pull requests.

### 3. Preserve provenance

New external evidence integrations should record enough provenance to explain where information came from and when it was retrieved.

### 4. Add regression coverage

Changes to workflow behaviour should add or update tests and, where appropriate, synthetic evaluation fixtures.

### 5. Keep the UI thin

Business logic belongs in the utility/orchestration layer rather than being duplicated inside Streamlit rendering code.

## Local verification

Run:

```bash
python -m compileall app.py config.py utils tests scripts
python -m unittest discover -s tests -p "test_*.py"
python scripts/evaluate.py
python scripts/evaluate_signals.py
python scripts/evaluate_reviews.py
```

## Pull requests

A useful pull request should explain what changed, why it changed, which workflow boundary is affected, what tests/evaluations were added or updated, and known limitations. Avoid unrelated refactors in feature commits; small, inspectable changes are easier to review.

## Scope

The project is a portfolio/development prototype. Production healthcare deployment would require a separate security, governance, clinical validation, and regulatory workstream.
