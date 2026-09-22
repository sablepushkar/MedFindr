# MedFindr v1.2 — SignalGraph Architecture

## System boundary

MedFindr remains a single Python/Streamlit prototype. v1.2 adds a structured information pipeline without adding a database, authentication layer, separate backend, or persistent patient records.

USER → UI → APPLICATION LOGIC → DATA/EVIDENCE → RESULT

1. Streamlit collects a bounded concern and optional public-label lookup term.
2. The response engine validates and normalizes the request.
3. Clinical information is extracted into a small structured model.
4. Data quality reports present and missing information.
5. The urgency engine generates a transparent prototype informational flag.
6. The safety-signal layer checks configured medication-exposure patterns.
7. The optional EBM layer provides explainable model output when available.
8. Evidence objects keep generated rules distinct from external information.
9. OpenFDA provides optional public label information with provenance.
10. The development trace records the ordered software stages in memory.
11. Streamlit renders the structured result.

## SignalGraph data flow

Free text
  ↓
Validation
  ↓
ClinicalContext
  ├── Symptoms
  ├── Medication context
  └── Temporal relationship
        ↓
  ┌─────┼────────┬────────┐
  ↓     ↓        ↓        ↓
Quality Urgency Safety    EBM
                 Signal
                   ↓
                Evidence
                   ↓
               Response
                   ↓
          Development Trace

## Key design choices

### Structured information before advanced intelligence

The project first represents the information it has. This creates a clean boundary for later terminology mapping, analytics, evidence adapters, or validated models.

### Signals are not conclusions

The safety layer uses explicit phrases and relationships. It uses terms such as potential, flagged, context incomplete, and review rather than claiming causality.

### Provenance is attached to evidence

Generated rule evidence identifies its rule source. Retrieved public label information identifies source, endpoint, query, and retrieval time. These evidence classes remain distinct.

### Trace without persistence

The trace provides development visibility into the workflow. It is in-memory and should not be described as a compliant audit log.

## Security/data boundary

- No authentication
- No patient account system
- No application database
- No patient-identifying data should be entered
- Bounded input lengths
- External failures handled without raw exception details in the UI

## Deliberately not added

- OMOP implementation
- FHIR server
- patient database
- authentication
- hospital/device connectivity
- real-time alerting
- autonomous diagnosis
- large language model orchestration
- microservices
- production cloud infrastructure

Those additions require additional requirements, validation, security controls, governance, and testing beyond this portfolio prototype.

## Extension points

Future modules can support standardized terminology mapping, literature/evidence adapters, pharmacovigilance datasets, validated ML models, research analytics, institutional APIs, event/device adapters, and persistent storage after an explicit privacy/security design.
