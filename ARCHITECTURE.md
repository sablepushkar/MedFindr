# MedFindr v2 Architecture

## System boundary

MedFindr v2 is a local/session-oriented information workflow:

```text
Input
  ↓
Validation
  ↓
Structured clinical information
  ↓
Data quality
  ↓
Urgency + medication-safety signals
  ↓
Optional EBM
  ↓
Evidence / OpenFDA retrieval
  ↓
Structured result + development trace
  ↓
Human review
  ↓
JSON review bundle
```

The architecture deliberately separates **information processing** from **human review**.

## Core modules

### `app.py`
Presentation layer.

Responsibilities:
- collect bounded user input
- trigger the analysis workflow
- render structured results
- expose technical details separately
- collect review fields
- provide JSON export

The UI should remain thin. Business logic belongs in `utils/`.

### `utils/response_engine.py`
Primary orchestration layer.

It coordinates validation, clinical extraction, data quality, urgency, safety signals, optional EBM, evidence, external retrieval, trace generation, and review-ready output.

### `utils/clinical_data.py`
Defines the normalized clinical-information representation.

The current prototype focuses on a small set of structured concepts rather than attempting full clinical NLP.

### `utils/data_quality.py`
Assesses whether important contextual fields are present.

Missing timing, severity, medication exposure, or other context can reduce interpretability. The application should surface those limitations instead of silently treating incomplete input as complete.

### `utils/urgency.py`
Contains the deterministic prototype urgency rules and regression-tested edge cases.

### `utils/safety_signals.py`
Produces medication-related software signals from structured information.

A signal means that a defined pattern was detected. It does not establish causality.

### `utils/ebm_risk.py`
Optional Explainable Boosting Machine layer.

The model is treated as an experimental/engineering component with fallback behaviour. Its output is not a clinical risk score.

### `utils/evidence.py`
Represents evidence and provenance.

The abstraction keeps evidence separate from conclusions so new evidence adapters can be introduced later.

### `utils/drug_lookup.py`
Retrieves public OpenFDA drug-label information defensively.

External responses are parsed into stable application structures and accompanied by provenance.

### `utils/analysis_trace.py`
Provides an in-memory development trace showing which stages were executed.

It is intentionally **not** a compliance audit log.

### `utils/review.py`
Defines the human review record.

The review record can capture:
- status
- evidence reviewed
- reviewer reasoning
- missing information
- follow-up requirement
- follow-up notes
- disposition
- completion timestamp

### `utils/review_export.py`
Serializes the review record into a JSON bundle for inspection or portfolio demonstration.

## Data flow

The application passes a structured response through the workflow instead of allowing each UI component to independently calculate results.

This creates a predictable boundary:

```text
Raw input
  → normalized input
  → structured clinical information
  → quality assessment
  → prototype signals
  → evidence
  → review-ready response
```

## Evidence architecture

Evidence objects are intentionally independent from the signal logic.

This allows future adapters to represent:

- public regulatory labels
- literature records
- pharmacovigilance datasets
- institutional sources
- validated internal datasets

Each external source should preserve provenance such as source type, source URL, query/identifier, and retrieval time where available.

## Human review boundary

The v2 review layer is not an automated clinical decision-maker.

The intended boundary is:

```text
Software
  → structures information
  → detects defined patterns
  → presents evidence
  → records limitations

Human reviewer
  → inspects information
  → records reasoning
  → requests follow-up
  → records a disposition
```

The current application does not persist these records in a production database.

## Security and privacy boundary

Current v2 deliberately has:

- no patient database
- no persistent patient records
- no production identity system
- no patient identifier model
- bounded input validation
- defensive external requests
- generic user-facing error handling
- synthetic evaluation fixtures

This is appropriate for a development-stage portfolio prototype, not a production healthcare deployment.

A production system would require a materially different security architecture: identity and access management, encryption, secrets management, audit infrastructure, data retention controls, monitoring, threat modelling, incident response, and organization-specific governance.

## Deliberate non-features

MedFindr v2 does not claim to be:

- a diagnostic engine
- a pharmacovigilance validation platform
- a causality-assessment system
- a clinical alerting service
- a treatment recommendation engine
- a production patient-record system

These boundaries are part of the engineering design.

## Verification

The repository uses:
- Python compilation checks
- unit/regression tests
- synthetic evaluation fixtures
- application import smoke testing
- GitHub Actions

The verification suite demonstrates software behaviour against defined fixtures. It is not clinical validation.

## Extension points

The current architecture can later support:

1. terminology mapping
2. richer temporal/event modelling
3. additional evidence adapters
4. validated datasets and ML experiments
5. institutional API adapters
6. device/event adapters
7. persistent review infrastructure
8. authenticated multi-user deployment

Any production-oriented extension should be introduced only with the required security, clinical, regulatory, and governance work.
