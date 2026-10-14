import json
import logging
from pathlib import Path

import streamlit as st

from config import APP_TITLE, APP_VERSION
from utils.response_engine import build_response
from utils.review import create_review_record, validate_review_record
from utils.review_export import serialize_review_bundle

logger = logging.getLogger(__name__)

# The rest of the existing page setup and render_structured_response function
# are preserved in the repository; this update targets the final response flow.
