"""Central configuration for MedFindr X1.2."""

from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
SAMPLE_CONCERNS_PATH = DATA_DIR / "sample_concerns.json"
EVALUATION_SET_PATH = DATA_DIR / "evaluation_set.json"

APP_NAME = "MedFindr"
APP_VERSION = "X1.2"
APP_CAPTION = "Structured health-concern prototype • Explainable risk • Drug-label lookup"

DISCLAIMER = (
    "This is a developmental portfolio prototype. It is not a substitute for "
    "professional medical advice, diagnosis, or treatment. Always consult a "
    "qualified healthcare professional for real health concerns."
)

OPENFDA_TIMEOUT = 10
OPENFDA_LABEL_URL = "https://api.fda.gov/drug/label.json"

EBM_MODEL_DIR = BASE_DIR / "models"
EBM_MODEL_PATH = EBM_MODEL_DIR / "ebm_urgency_model.pkl"
