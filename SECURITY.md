# Security and privacy notes

MedFindr is a learning prototype. It has not been reviewed or approved for use with real patient information.

## Please do not

- Enter names, contact details, medical record numbers or other identifying patient data.
- Use the result to decide whether to start, stop or change a medicine.
- Treat a rule flag as a diagnosis or a validated urgency assessment.
- Commit secrets, access tokens or private datasets to this repository.

## Current limits

The app does not provide user accounts or a protected patient database. Review information is handled in the current Streamlit session and can be exported by the user; it is not a governed audit system. Public drug-label lookup may fail or return information that needs to be checked at its source.

If you find a security issue in the code, please describe the affected file and a safe way to reproduce it without sharing private data.
