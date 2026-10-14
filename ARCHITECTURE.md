# MedFindr — how the app is organised

## Current setup

MedFindr is one Python application built with Streamlit. The interface, rule logic and source lookup are separate parts of the code, but they run as one app.

## Main path

1. The user enters a short concern and may enter a medicine name.
2. The app checks and normalises the input.
3. The rule code looks for a limited set of phrases and context.
4. Optional model output or fallback behaviour is shown separately from the rule result.
5. If requested, the app looks up public drug-label data.
6. The result shows what MedFindr generated and what came from the external source.
7. The user can fill in a review form and export it as JSON.

## What is present

- Streamlit interface and response flow.
- Rule-based phrase checks.
- Optional local model loading with fallback behaviour.
- Public drug-label lookup.
- Source metadata and evidence records.
- Small evaluation scripts and regression tests.
- Session-based review form and JSON export.

## What is not present

There is no user-account system, patient database, persistent review database, hospital integration or production deployment. The trace helper is for debugging and is not an audit log. The app does not use a clinically validated model.

## Why I am keeping it small

Adding authentication, a database or several services would make the project harder to maintain without solving the problems I am testing right now. I want the rules, lookup failures and evaluation results to be understandable first.

## Data and safety

The public lookup data is not the same thing as MedFindr's own rule output. The app should keep those sources distinct. No secrets should be committed, and no real patient-identifying information should be entered. This project is for learning and software experiments, not diagnosis or treatment decisions.
