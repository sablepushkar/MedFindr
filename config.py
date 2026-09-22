"""Application configuration for MedFindr v2."""
from __future__ import annotations
from pathlib import Path
BASE_DIR=Path(__file__).resolve().parent
DATA_DIR=BASE_DIR/"data"
APP_NAME="MedFindr"
APP_VERSION="v2.0"
APP_CAPTION="Med × Pharma • structured information • transparent signals • human review workflow"
DISCLAIMER="MedFindr is a development-stage information prototype. It does not diagnose conditions, establish causality, recommend treatment, replace a clinician or pharmacist, or provide validated clinical alerts."
SAMPLE_CONCERNS_PATH=DATA_DIR/"sample_concerns.json"
OPENFDA_TIMEOUT=10
OPENFDA_LABEL_URL="https://api.fda.gov/drug/label.json"
EBM_MODEL_PATH=BASE_DIR/"models"/"ebm_risk.joblib"
EBM_META_PATH=BASE_DIR/"models"/"ebm_meta.json"
