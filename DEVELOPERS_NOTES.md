# MedFindr Developer Notes — v2.0

## Objective

Turn the v1.2 SignalGraph prototype into a small, inspectable human-in-the-loop healthcare/pharma information workflow.

## v2 implementation

The current v2 development branch adds:

- structured human review records
- review status and disposition
- reviewer reasoning
- evidence-reviewed tracking
- missing-information tracking
- follow-up requirement and notes
- completion timestamps
- JSON review-bundle export
- synthetic review evaluation fixtures
- dedicated review regression tests
- Streamlit review workflow
- professional repository documentation and security/contribution boundaries

## Engineering principle

The project is deliberately moving from:

```text
input → signal → output
```

toward:

```text
input
→ structure
→ quality
→ signal
→ evidence
→ human review
→ exportable record
```

The second workflow is more representative of how a future healthcare/pharma software component could fit into a larger process without pretending that the prototype itself is a validated clinical product.

## Presentation audit

The public repository presentation was revised around patterns found in established healthcare/pharma software repositories:

- one-line product definition
- at-a-glance capability table
- explicit problem statement
- workflow/architecture
- evidence and data provenance
- measurable evaluation
- quickstart
- security/privacy boundary
- roadmap
- ownership and limitations

The goal is to make the repository readable as a serious engineering portfolio project while keeping the claims proportional to the actual implementation.

## Deliberate non-features

v2 still does not add:

- real patient data
- patient persistence
- production authentication
- institutional integration
- clinical alerting
- automated treatment recommendations
- claims of clinical validation

## Verification target

Every v2 feature should follow:

```text
implement
→ compile
→ test
→ inspect integration
→ fix
→ retest
```

The GitHub Actions workflow is part of that verification boundary.

## Authorship

MedFindr is a student-built project created and directed by Pushkar Sable. External assistance may be used selectively for research, implementation support, debugging, and review; repository decisions and final acceptance remain with the project creator.

## Current branch policy

`v2-development` is the active development branch for this release line.

The `main` branch is not changed by this documentation pass. Promotion should happen only after the v2 implementation and verification are deliberately reviewed.
