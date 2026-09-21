"""
Basic configuration for MedFindr.
Kept simple and centralised so future changes stay clean.
"""

from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
SAMPLE_CONCERNS_PATH = DATA_DIR / "sample_concerns.json"
EVALUATION_SET_PATH = DATA_DIR / "evaluation_set.json"

# App metadata
APP_NAME = "MedFindr"
APP_VERSION = "07.3 major"
APP_CAPTION = "Developmental prototype · Not medical advice"

# Safety
DISCLAIMER = (
    "This is an early developmental version of MedFindr. "
    "It is not a substitute for professional medical advice, diagnosis, or treatment. "
    "Always consult a qualified healthcare provider for any health concern."
)

# API
OPENFDA_TIMEOUT = 10
OPENFDA_LABEL_URL = "https://api.fda.gov/drug/label.json"
