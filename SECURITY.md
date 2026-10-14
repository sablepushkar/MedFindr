# Security & Privacy

## Current status

MedFindr is a development-stage healthcare/pharmaceutical information prototype. It is not approved for real patient information or production healthcare deployment.

## Data policy

Use only synthetic data, public/non-sensitive examples, and information that contains no patient identifiers. Do not commit real patient information to the repository, issues, pull requests, screenshots, test fixtures, or exported examples.

## Current security boundary

The current application includes bounded input validation, defensive parsing of external responses, generic user-facing error messages, and public OpenFDA drug-label retrieval. It does not provide a patient database, persistent patient-record store, production authentication/authorization, patient-identity model, or institutional integration. Review records are session-scoped and JSON exports are generated only on user request; neither is a governed audit log.

The absence of a patient database is deliberate for this prototype, but it does not by itself make arbitrary use safe.

## External data

External responses are untrusted input and are parsed defensively. Network failures and malformed responses should be handled without exposing raw exception details through the normal UI. Retrieved label content must remain distinguishable from MedFindr-generated rule flags.

## Reporting a security issue

For a genuine security concern, avoid publishing sensitive exploit details in a public issue. Use GitHub's private security reporting mechanisms when available for the repository. For ordinary development bugs, use a normal issue or pull request without including sensitive medical information.

## Production gap

A real healthcare deployment would require stronger controls, including identity and access management, least-privilege authorization, encryption in transit and at rest, secrets management, audit logging, data retention/deletion controls, threat modelling, dependency and vulnerability management, monitoring and incident response, organization-specific governance, and clinical validation/regulatory review where applicable.

This document describes the current prototype boundary; it is not a claim of production compliance.
