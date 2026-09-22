# MedFindr v1.2

**Med × Pharma × Data × Technology**

MedFindr is an actively developed healthcare/pharmaceutical technology prototype exploring medical information discovery, transparent informational flagging, structured data handling, evidence provenance, and future healthcare/pharma workflow integration.

## Current status

**v1.2 — SignalGraph prototype**

v1.2 adds a focused information-engineering layer rather than a generic chatbot. The prototype converts supplied text into structured findings, evaluates medication-related information patterns, attaches evidence/provenance objects, reports input completeness, and records an in-memory development trace.

### Current workflow

USER → STREAMLIT UI → VALIDATION → STRUCTURED CLINICAL INFORMATION → DATA QUALITY → URGENCY + SAFETY SIGNALS → EBM → EVIDENCE/OPENFDA → STRUCTURED RESULT + TRACE

The repository currently has no application database, authentication system, or separate backend service. This remains deliberate: v1.2 demonstrates the information pipeline without unnecessary persistence or patient-account complexity.

## SignalGraph

SignalGraph is MedFindr's lightweight normalized information pipeline.

It currently represents:
- supported symptom concepts
- optional medication context
- temporal medication relationship when explicitly stated
- context terms
- prototype medication-related safety signals
- evidence/provenance objects
- input completeness indicators
- ordered development stages

A safety signal means an information pattern worth review by the prototype. It does not mean that a medicine caused an adverse event and does not establish diagnosis, treatment, or clinical risk.

## What works now

- Bounded free-text validation
- Lightweight normalized clinical-information model
- Transparent rule-based prototype informational flags
- Medication-related safety-signal pattern detection
- Evidence objects separating generated signals from retrieved information
- Data-quality/completeness indicator
- In-memory development trace with generated analysis identifier
- Optional Explainable Boosting Machine layer with explicit fallback
- OpenFDA public label retrieval with timeout/error handling and source provenance
- General and Technical UI modes
- Synthetic SignalGraph evaluation fixture
- Existing urgency evaluation with confusion matrix and per-class metrics
- Automated regression checks through GitHub Actions

## Architecture

Presentation: app.py renders structured results.

Application pipeline: utils/response_engine.py orchestrates the workflow.

Structured information: utils/clinical_data.py converts bounded free text into a small normalized model. This is inspired by healthcare data-standardization principles but is not an implementation of OMOP or another common data model.

Signal layer: utils/safety_signals.py detects configured medication-exposure patterns and intentionally avoids causal language.

Evidence layer: utils/evidence.py represents both MedFindr-generated rule evidence and externally retrieved label information.

External data: utils/drug_lookup.py isolates OpenFDA public label retrieval and attaches source metadata.

Trace: utils/analysis_trace.py records ordered software stages in memory. It is a development trace, not a compliant audit log.

## Technologies

- Python
- Streamlit
- Requests
- pandas / NumPy
- scikit-learn
- InterpretML
- joblib
- GitHub Actions

## Run locally

    python -m pip install -r requirements.txt
    streamlit run app.py

Regression suite:

    python -m unittest discover -s tests -v

Evaluations:

    python scripts/evaluate.py
    python scripts/evaluate_signals.py

## Security and data handling

- Application secrets are not stored in source code.
- .env and Streamlit secrets files are ignored by Git.
- User input is bounded and normalized.
- External API failures do not expose raw exception details to the UI.
- No patient records are persisted.
- Do not enter real patient-identifying information.

## Medical/pharma scope

MedFindr separates retrieved public label information from prototype analysis.

The safety-signal layer is a software-pattern detector for development and portfolio demonstration. It is not pharmacovigilance validation, adverse-event causality assessment, diagnostic reasoning, medical advice, or a clinical alert system.

The OpenFDA adapter is used as a public information source. OpenFDA states that its data should not be relied on for medical-care decisions and that results may be unvalidated; MedFindr therefore presents retrieved label information separately from generated prototype signals.

## Deliberate non-features

v1.2 does not add patient accounts, authentication, persistent health records, hospital/device integrations, real-time clinical alert infrastructure, autonomous diagnosis, a large LLM/chatbot layer, microservices, or production cloud infrastructure.

These remain future research/integration directions rather than claims about the current prototype.

## Evaluation

The repository includes a 15-case urgency regression fixture and a separate synthetic medication-signal fixture with automated unit/contract tests. Results describe software behavior on these fixtures only; they do not establish clinical safety, efficacy, pharmacovigilance performance, or generalization.

## Future direction

Potential future work includes richer biomedical/pharma datasets, controlled literature retrieval, standardized terminology mapping, pharmacovigilance research workflows, biomedical knowledge graphs, validated ML experiments, institutional APIs, device/event inputs, and analytics over non-sensitive structured data.

The project should remain a serious student-built healthcare/pharma technology prototype rather than a simulated commercial medical platform.

## Development principle

inspect → plan → modify → test → fix → retest

Build the foundation, not the fantasy.
