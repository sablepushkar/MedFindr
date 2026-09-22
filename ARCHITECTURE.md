# MedFindr v2 Architecture

## System boundary
MedFindr v2 is a local/session-oriented information workflow: `input → validation → structure → quality → signals → evidence → review → export`.

The application has no application database and no patient-account layer.

## Core design
### Structured information before intelligence
The pipeline creates a normalized representation before later analysis stages.
### Signals are not conclusions
Urgency and medication-safety rules are prototype software signals. They do not establish diagnosis, causality, treatment need, or clinical severity.
### Evidence carries provenance
Evidence objects identify evidence type and source. Retrieved public-label information remains distinguishable from MedFindr-generated rule evidence.
### Human review is explicit
`ReviewRecord` captures review status, evidence reviewed, reasoning, missing information, follow-up requirement, follow-up notes, disposition, and review timestamp.
### Export without persistence
A review bundle can be downloaded as JSON. The export does not imply that MedFindr stores the record.

## Data and privacy boundary
The v2 prototype deliberately avoids patient identifiers and persistent clinical storage. It should not be described as an EHR, pharmacovigilance database, or compliance audit system.

If persistence is introduced later, authentication/authorization, encrypted storage, retention/deletion rules, access logging, privacy review, data minimization, and governance must be designed separately.

## Failure handling
- validation errors stop analysis early
- external retrieval failures remain isolated
- unexpected UI pipeline errors are logged server-side and shown generically
- review validation blocks incomplete follow-up records
- export contains explicit limitations

## Verification
CI compiles the repository, imports the application, runs regression tests, and executes synthetic evaluation scripts.

## Extension points
Terminology adapters, evidence source adapters, validated pharmacovigilance datasets, model benchmarking, secure persistence, institutional integrations, and device/event ingestion can be added behind the current module boundaries.
