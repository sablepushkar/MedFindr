# SignalGraph and Human Review Scope

MedFindr's SignalGraph layer extends the structured information workflow with a small human-in-the-loop review path.

Core flow: `input → structure → quality → signal → evidence → review → disposition → export`.

The review layer is intentionally in-memory and development-stage. It is not a patient record system, compliance audit log, pharmacovigilance database, diagnostic system, or clinical alert service.

## Current capabilities

- normalized phrase-matched symptom and medication context
- prototype medication-related safety signals
- explicit input-completeness indicator
- evidence and provenance objects
- review status and disposition
- reviewer notes and follow-up capture
- session-scoped review state
- user-triggered JSON review bundle export
- synthetic evaluation fixtures and regression tests

## Review model

A review record can contain an analysis identifier, review status, evidence reviewed, reviewer reasoning, follow-up requirement, missing information, disposition, and review timestamp. The application does not collect or persist a dedicated patient identifier.

Phrase matching is intentionally limited; direct-negation patterns reduce obvious false matches but do not make the extraction clinically reliable. Every included evaluation tests software behavior only, not clinical validity.
