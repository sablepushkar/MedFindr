# MedFindr — Developer Notes

## v1.2 — SignalGraph prototype

v1.2 builds on the v1.1 reliability foundation without replacing the working architecture.

### Changes

- Added a lightweight normalized clinical-information model.
- Added medication-exposure relationship extraction.
- Added a prototype medication-related safety-signal layer.
- Added explicit evidence/provenance objects.
- Added input completeness/data-quality reporting.
- Added an in-memory analysis trace with an analysis identifier.
- Extended the Staff view to expose structured data and trace information.
- Added a synthetic signal-evaluation dataset and evaluation script.
- Preserved the existing urgency engine, EBM boundary, OpenFDA adapter, validation layer, and regression suite.
- Updated release and architecture documentation.

### Engineering boundary

The signal layer is intentionally a pattern detector. It does not infer that a drug caused an event, diagnose, prescribe, recommend treatment, or act as a clinical alerting system.

### Deliberately unchanged

- Existing urgency rules and regression fixes
- Cached EBM loading boundary
- OpenFDA retrieval boundary
- No-database architecture
- No-authentication architecture
- Small-project implementation style

### Deliberately not implemented

OMOP/FHIR implementation, patient records, authentication, hospital/device integrations, real-time alerting, autonomous diagnosis, large AI/LLM features, and production infrastructure.

### Verification target

The v1.2 candidate should pass Python compilation, regression tests, SignalGraph tests, urgency evaluation, synthetic signal evaluation, and GitHub Actions checks.

Evaluation fixtures are software-development tests, not clinical or pharmacovigilance validation.

### Project authorship

MedFindr is a student-built project created by Pushkar Sable. External assistance is used selectively for debugging, research, review, and implementation support; the project concept, direction, scope decisions, and repository ownership remain the creator's.
