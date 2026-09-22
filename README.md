# MedFindr v2

**Structured healthcare & medication-safety information workflow — with evidence provenance and human review.**

[![MedFindr checks](https://github.com/sablepushkar/MedFindr/actions/workflows/medfindr.yml/badge.svg)](https://github.com/sablepushkar/MedFindr/actions/workflows/medfindr.yml)

MedFindr is a **student-built healthcare/pharma technology prototype** for turning a free-text health/medication concern into structured information, transparent prototype signals, evidence references, and a human review record.

It is designed as a portfolio engineering project: the emphasis is on **workflow design, explainability, provenance, evaluation, testing, and clear safety boundaries**, rather than presenting an unvalidated model as a clinical system.

## At a glance

| Area | Current v2 |
|---|---|
| Interface | Streamlit |
| Core language | Python |
| Structured layer | Clinical information + SignalGraph |
| Signal logic | Deterministic prototype rules + optional EBM |
| Evidence | Internal rule evidence + public OpenFDA label retrieval |
| Human workflow | Review status, reasoning, missing information, follow-up, disposition |
| Output | Structured result + JSON review bundle |
| Persistence | None; session/in-memory workflow |
| Data | Synthetic evaluation fixtures; no real patient dataset |
| Verification | Unit tests, synthetic evaluations, GitHub Actions |

## Why this project exists

Healthcare and pharma workflows often depend on information arriving in different forms: symptoms, medication exposure, timing, context, evidence, and human review.

MedFindr explores a small software architecture for making those steps explicit instead of hiding everything behind a single prediction.

The project asks:

> How can a healthcare/pharma information workflow make its inputs, signals, evidence, uncertainty, and human decisions easier to inspect?

## Core workflow

```text
USER INPUT
   ↓
VALIDATION
   ↓
STRUCTURED CLINICAL INFORMATION
   ↓
DATA QUALITY
   ↓
URGENCY + MEDICATION SAFETY SIGNALS
   ↓
OPTIONAL EBM RISK ESTIMATE
   ↓
EVIDENCE / PUBLIC LABEL RETRIEVAL
   ↓
STRUCTURED RESULT
   ↓
HUMAN REVIEW WORKSPACE
   ↓
JSON REVIEW BUNDLE
```

### Human-in-the-loop review

The v2 workflow does not treat a generated signal as a final conclusion.

A reviewer can record:

- review status
- evidence reviewed
- reviewer reasoning
- missing information
- whether follow-up is required
- follow-up notes
- final disposition
- completion timestamp

This creates a small but explicit **decision-support workflow boundary**: software produces structured information and signals; a human records the review outcome.

## What the repository demonstrates

### 1. Structured information before advanced intelligence

The application first normalizes the input into concepts such as:

- concern/symptoms
- medication exposure
- timing/context
- severity
- data completeness

This makes later rules, evidence adapters, or validated models easier to replace or extend.

### 2. Transparent signals

MedFindr can surface prototype medication-safety patterns and urgency categories while keeping the language deliberately non-diagnostic.

A signal is an **engineering output**, not a clinical causality assessment.

### 3. Evidence provenance

External information is represented with provenance such as source, retrieval time, query, and source type.

The current public external source is OpenFDA drug-label information. The repository keeps the evidence layer separate so future literature, regulatory, or institutional adapters can be added without rewriting the workflow.

### 4. Human review

The review layer captures the information a human would need to inspect before treating a signal as actionable within a future workflow.

### 5. Evaluation rather than unsupported claims

Synthetic fixtures are used to test:

- urgency classification
- SignalGraph extraction
- medication-safety signal detection
- review workflow contracts

The repository reports software/evaluation results as engineering verification. They are **not clinical validation metrics**.

## Example workflow

A synthetic concern such as a symptom occurring after medication exposure can be processed as:

1. validate the text and medication input
2. extract structured clinical information
3. assess information completeness
4. generate urgency and medication-safety signals
5. optionally calculate an EBM prototype estimate
6. attach available evidence
7. retrieve public label information when requested
8. display the structured SignalGraph result
9. record human review fields
10. export the review bundle as JSON

## Architecture

```text
app.py
  │
  └── response_engine.py
        ├── validation.py
        ├── clinical_data.py
        ├── data_quality.py
        ├── urgency.py
        ├── safety_signals.py
        ├── ebm_risk.py
        ├── evidence.py
        ├── drug_lookup.py
        ├── analysis_trace.py
        └── review.py / review_export.py

data/
  ├── synthetic evaluation fixtures
  └── sample concerns

tests/
  ├── urgency regression tests
  ├── SignalGraph tests
  └── review workflow tests

scripts/
  ├── evaluate.py
  ├── evaluate_signals.py
  ├── evaluate_reviews.py
  └── train_ebm.py
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for the current system boundary and design decisions.

## Evidence and external data

The current external integration uses the public OpenFDA drug-label API for label retrieval.

MedFindr treats retrieved information as **evidence to inspect**, not as an automated medical recommendation. External retrieval can fail, return incomplete information, or change independently of this repository.

The evidence abstraction is intentionally designed for future adapters such as:

- regulatory sources
- literature/evidence services
- pharmacovigilance datasets
- institutional APIs
- validated internal datasets

## Evaluation & verification

The repository includes automated checks for the current prototype.

Local verification:

```bash
python -m compileall app.py config.py utils tests scripts
python -m unittest discover -s tests -p "test_*.py"
python scripts/evaluate.py
python scripts/evaluate_signals.py
python scripts/evaluate_reviews.py
```

GitHub Actions also checks compilation, application import, regression tests, and synthetic evaluation scripts.

**Important:** passing software tests means the implementation matches its defined test fixtures. It does not establish clinical safety, diagnostic accuracy, pharmacovigilance validity, or regulatory compliance.

## Quick start

### 1. Clone

```bash
git clone https://github.com/sablepushkar/MedFindr.git
cd MedFindr
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Run

```bash
streamlit run app.py
```

### 4. Try a synthetic example

Use the sample concerns available in the application sidebar. Avoid entering real patient-identifying or sensitive medical information.

## Repository map

| Path | Purpose |
|---|---|
| `app.py` | Streamlit interface and review workflow |
| `utils/response_engine.py` | Main orchestration layer |
| `utils/clinical_data.py` | Structured clinical information |
| `utils/safety_signals.py` | Prototype medication-safety signals |
| `utils/evidence.py` | Evidence/provenance objects |
| `utils/drug_lookup.py` | OpenFDA retrieval |
| `utils/review.py` | Human review record |
| `utils/review_export.py` | JSON review-bundle export |
| `tests/` | Regression and workflow tests |
| `scripts/` | Evaluation and model tooling |
| `ARCHITECTURE.md` | System design |
| `V2_SCOPE.md` | v2 scope and engineering boundary |
| `DEVELOPERS_NOTES.md` | Development decisions and verification history |

## Security & privacy boundary

MedFindr v2 deliberately does **not** include:

- a patient database
- production authentication/authorization
- persistent patient records
- a patient identifier model
- institutional clinical integrations
- a validated clinical alerting service

Current protections include bounded input validation, defensive external retrieval, generic user-facing errors, and synthetic/non-sensitive evaluation data.

For a real healthcare deployment, the architecture would require substantially stronger controls including identity/access management, audit infrastructure, encryption, data retention policies, secrets management, monitoring, threat modelling, clinical validation, regulatory review, and institution-specific governance.

See [SECURITY.md](SECURITY.md).

## Roadmap

### v2 — current direction
- structured healthcare information
- transparent safety signals
- evidence provenance
- human review workspace
- review export
- synthetic evaluation
- CI verification

### v3 — possible future research direction
- terminology normalization
- richer evidence/literature adapters
- pharmacovigilance datasets
- stronger temporal/event modelling
- validated ML experiments
- institutional API adapters
- non-sensitive workflow analytics
- deployment architecture appropriate to a real organization

These are roadmap directions, not claims about current functionality.

## Project ownership

**MedFindr is a student-built project created and directed by Pushkar Sable.**

The creator owns the project concept, repository, scope decisions, architecture direction, feature priorities, testing acceptance, and roadmap. Selective external assistance has been used for research, implementation support, debugging, and review.

The repository is intentionally documented so that the implementation choices and limitations can be inspected rather than presented as a black box.

## Disclaimer

MedFindr is a **development-stage information-engineering and portfolio prototype**.

It does not diagnose conditions, establish causality, recommend treatment, replace clinicians or pharmacists, or provide validated clinical alerts. Do not use its outputs as a substitute for professional medical judgement.

See [V2_SCOPE.md](V2_SCOPE.md) and [ARCHITECTURE.md](ARCHITECTURE.md) for scope details.

## License

See [LICENSE](LICENSE).
