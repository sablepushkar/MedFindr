"""Central configuration for MedFindr v1.2."""
from pathlib import Path
BASE_DIR=Path(__file__).parent
DATA_DIR=BASE_DIR/"data"
SAMPLE_CONCERNS_PATH=DATA_DIR/"sample_concerns.json"
EVALUATION_SET_PATH=DATA_DIR/"evaluation_set.json"
SIGNAL_EVALUATION_PATH=DATA_DIR/"signal_evaluation_set.json"
APP_NAME="MedFindr"
APP_VERSION="v1.2"
APP_CAPTION="Med × Pharma • SignalGraph • evidence-linked prototype analysis"
DISCLAIMER=("MedFindr is an actively developed healthcare/pharmaceutical technology prototype. "
"It organizes information and generates transparent prototype signals; it is not a certified "
"medical device, clinically validated system, hospital-ready product, diagnostic system, or "
"autonomous medical decision-maker. Do not enter real patient-identifying information.")
OPENFDA_TIMEOUT=10
OPENFDA_LABEL_URL="https://api.fda.gov/drug/label.json"
EBM_MODEL_DIR=BASE_DIR/"models"
EBM_MODEL_PATH=EBM_MODEL_DIR/"ebm_urgency_model.pkl"
