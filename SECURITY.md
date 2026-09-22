# Security & Privacy

## Current status

MedFindr v2 is a **development-stage portfolio prototype**. It is not approved for real patient information or production healthcare deployment.

## Data policy

Use only:
- synthetic data
- public/non-sensitive examples
- information that contains no patient identifiers

Do not commit real patient information to the repository, issues, pull requests, screenshots, test fixtures, or exported examples.

## Current security boundary

The current application has:

- bounded input validation
- defensive parsing of external responses
- generic user-facing error messages
- no patient database
- no persistent patient record store
- no production authentication/authorization
- no patient identifier model
- no institutional integration
- no production secrets requirement

The absence of a database is deliberate. It limits the current project's data exposure while the workflow is being developed.

## External data

MedFindr can retrieve public OpenFDA drug-label information.

External responses are treated as untrusted input and are parsed defensively. Network failures and malformed responses are handled without exposing raw exception details through the normal UI.

## Reporting a security issue

For a genuine security concern, avoid publishing sensitive exploit details in a public issue. Use GitHub's private security reporting mechanisms when available for the repository.

For ordinary development bugs, use a normal issue or pull request without including sensitive medical information.

## Production gap

A real healthcare deployment would require substantially stronger controls, including:

- identity and access management
- least-privilege authorization
- encryption in transit and at rest
- secrets management
- audit logging
- data retention/deletion controls
- threat modelling
- dependency and vulnerability management
- monitoring and incident response
- organization-specific governance
- clinical validation and regulatory review where applicable

This document describes the current prototype boundary; it is not a claim of production compliance.
