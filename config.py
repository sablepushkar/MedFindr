"""
Central configuration for MedFindr.
"""

from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
SAMPLE_CONCERNS_PATH = DATA_DIR / "sample_concerns.json"
EVALUATION_SET_PATH = DATA_DIR / "evaluation_set.json"

APP_NAME = "MedFindr"
APP_VERSION = "08.1 Beta testing EBM"
APP_CAPTION = "Developmental prototype · Not medical advice"

DISCLAIMER = (
    "This is an early developmental version of MedFindr. "
    "It is not a substitute for professional medical advice, diagnosis, or treatment. "
    "Always consult a qualified healthcare provider for any health concern."
)

OPENFDA_TIMEOUT = 10
OPENFDA_LABEL_URL = "https://api.fda.gov/drug/label.json"

# EBM related (future model path)
EBM_MODEL_DIR = BASE_DIR / "models"
