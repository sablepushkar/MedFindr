# MedFindr v1.1 — Architecture Audit

## Current system boundary

MedFindr is currently a single Python/Streamlit prototype. It is not a full-stack application yet.

### USER → UI → APPLICATION LOGIC → API/DATA → RESULT

1. User enters a free-text health concern and optionally a lookup term.
2. Streamlit UI collects input and submits through one form.
3. Input validation normalizes text and enforces bounded inputs.
4. Response engine orchestrates the workflow.
5. Urgency layer produces a transparent prototype informational flag.
6. EBM layer optionally loads a compatible local model or exposes a fallback.
7. External data layer retrieves structured label information from the configured public source.
8. Structured response combines generated analysis and retrieved information while keeping provenance attached to external data.
9. UI renders results, errors, scope notes, and source metadata.

## Audit findings

### Working and retained

- Thin Streamlit presentation layer
- Modular response engine
- Rule-based urgency engine
- Cached optional model loading
- External-data isolation
- Regression/evaluation tooling
- Existing evaluation edge-case fixes

### Improved in v1.1

- Bounded input validation
- Defensive parsing of external API responses
- Stable user-facing error messages
- Source provenance for retrieved records
- Explicit distinction between informational flags and retrieved data
- Form-based submission to reduce accidental repeated actions
- Mobile-friendly centered layout and full-width primary action
- Staff-only technical detail remains opt-in
- Automated regression workflow
- Clear architecture and scope documentation

### Deliberately not added

- Database
- Authentication
- Patient accounts
- Persistent health records
- Hospital/device integrations
- Real-time alert infrastructure
- Autonomous diagnosis
- Large AI/LLM layer
- Complex microservices
- Production cloud infrastructure

Those additions would increase system complexity without solving a current v1.1 reliability problem.

## Security review

No application secret is hard-coded in the current source. Local environment/secrets files are ignored. The current prototype does not implement authentication because it does not have user accounts or protected data.

## Data/provenance model

External records carry:

- source name
- source type
- source endpoint
- query
- retrieval timestamp

System-generated analysis is labelled separately and should never be presented as retrieved clinical evidence.

## Extension points

Future modules can be added behind the response-engine boundary:

- evidence/data retrieval
- structured pharmaceutical data
- analytics
- validated ML models
- institutional API adapters
- research workflows

The current architecture intentionally keeps these as extension points rather than pretending they already exist.
