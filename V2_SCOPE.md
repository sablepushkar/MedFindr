# MedFindr v2 Scope

MedFindr v2 extends the v1.2 SignalGraph prototype into a small human-in-the-loop healthcare/pharma information workflow.

Core flow: `input → structure → quality → signal → evidence → review → disposition → export`

The review layer is intentionally in-memory and development-stage. It is not a patient record system, compliance audit log, pharmacovigilance database, diagnostic system, or clinical alert service.

## v2 capabilities
- normalized clinical/medication information
- prototype medication-related safety signals
- explicit input completeness
- evidence and provenance objects
- human review status and disposition
- reviewer reasoning and follow-up capture
- session-scoped review state
- exportable structured JSON review bundle
- synthetic review fixtures and regression tests

## Review model
A review record can contain an analysis identifier, review status, signal context, evidence reviewed, reviewer reasoning, follow-up requirement, missing information, final disposition, and review timestamp.

No patient identifier is collected or persisted by the application.

Every v2 feature is evaluated as software behavior, not clinical validity.
