"""Export helpers for MedFindr v2 review bundles."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
import json
def build_review_bundle(response: Any, review: Any) -> dict[str, Any]:
    return {"format":"medfindr-review-bundle","format_version":"2.0","exported_at_utc":datetime.now(timezone.utc).isoformat(),"analysis":response.to_dict(),"review":review.to_dict(),"limitations":["Development-stage prototype output.","Review state is session-scoped and not a compliance audit log.","Signals are not diagnoses or causality assessments.","Software evaluation is not clinical validation."]}
def serialize_review_bundle(response: Any, review: Any) -> str:
    return json.dumps(build_review_bundle(response, review), indent=2, sort_keys=True)
