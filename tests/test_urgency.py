"""Regression and contract tests for the MedFindr v1.2 prototype."""
from __future__ import annotations

import json
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from utils.drug_lookup import search_drug
from utils.response_engine import build_response
from utils.urgency import assess_urgency
from utils.validation import validate_concern, validate_drug_name

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "evaluation_set.json"

# Existing regression/contract tests retained from the v1.1 reliability layer.
# The labelled evaluation fixture is intentionally small and is not clinical validation.
