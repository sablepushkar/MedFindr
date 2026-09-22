"""Central configuration for MedFindr v1.1."""

from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
SAMPLE_CONCERNS_PATH = DATA_DIR / "sample_concerns.json"
EVALUATION_SET_PATH = DATA_DIR / "evaluation_set.json"

APP_NAME = "MedFindr"
APP_VERSION = "v1.1"
APP_CAPTION = "Med × Pharma • structured information • transparent prototype flags"

DISCLAIMER = (
    "MedFindr is an actively developed healthcare/pharmaceutical technology "
    "prototype. It is not a certified medical device, clinically validated system, "
    "hospital-ready product, diagnostic system, or autonomous medical decision-maker. "
    "Prototype flags are informational only. Consult a qualified healthcare professional "
    "for real health concerns."
)

OPENFDA_TIMEOUT = 10
OPENFDA_LABEL_URL = "https://api.fda.gov/drug/label.json"

EBM_MODEL_DIR = BASE_DIR / "models"
EBM_MODEL_PATH = EBM_MODEL_DIR / "ebm_urgency_model.pkl"
