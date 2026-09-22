# MedFindr — Developer Notes

## X1.2 — Consolidated working release

X1.2 consolidates the verified development work onto the main branch. The release is based on the known-good X1.0+ baseline and incorporates the useful efficiency refinements from the interrupted main-branch work without carrying forward its temporary corrupted states.

### Engineering changes

- Urgency patterns are normalized once per request.
- Duplicate urgency reasons are prevented.
- Known evaluation edge cases are covered by explicit regression rules/tests.
- EBM model loading is cached after its first attempt.
- The response engine keeps urgency, EBM, and drug lookup as separate layers.
- The Streamlit UI remains a presentation layer over the testable pipeline.
- The evaluation script is runnable from the repository root.
- Release metadata and documentation identify X1.2 consistently.

### Verification state

The bundled regression/evaluation workflow was checked during the X1.2 consolidation. The current labelled evaluation set passes its expected urgency labels, and the Python modules were compile-checked.

The evaluation set is a small software regression fixture. Its results do not establish clinical safety, diagnostic accuracy, or treatment effectiveness.

## Recovered branch history

- 470031a — verified X1.0+ baseline.
- v2-development — controlled repair/development branch.
- 49245e5 — final verified V2 tip before X1.2 promotion.
- main — consolidated X1.2 working branch.

The older interrupted commits remain in Git history for traceability and were not treated as a source of production behaviour.

## Portfolio engineering rule

MedFindr is a portfolio prototype, not a clinical decision system. Medical, drug, or workflow claims must remain auditable, clearly scoped, and backed by explicit data sources. Future features should be introduced as small independently testable changes rather than large unverified rewrites.
