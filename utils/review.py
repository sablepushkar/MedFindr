"""Human-in-the-loop review objects for MedFindr v2."""
from __future__ import annotations
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional
import json
REVIEW_STATUSES = ("new", "in_review", "awaiting_follow_up", "reviewed")
DISPOSITIONS = ("unresolved", "informational", "follow_up_required", "closed_for_review")
@dataclass
class ReviewRecord:
    analysis_id: str
    status: str = "new"
    evidence_reviewed: list[str] = field(default_factory=list)
    reviewer_reasoning: str = ""
    follow_up_required: bool = False
    follow_up_notes: str = ""
    missing_information: list[str] = field(default_factory=list)
    disposition: str = "unresolved"
    reviewed_at_utc: Optional[str] = None
    def mark_reviewed(self) -> None:
        self.status = "reviewed"
        self.reviewed_at_utc = datetime.now(timezone.utc).isoformat()
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)
def create_review_record(response: Any) -> ReviewRecord:
    trace = getattr(response, "trace", None)
    analysis_id = getattr(trace, "analysis_id", "") if trace else ""
    quality = getattr(response, "data_quality", None)
    missing = list(getattr(quality, "missing", []) or []) if quality else []
    return ReviewRecord(analysis_id=analysis_id, missing_information=missing)
def validate_review_record(record: ReviewRecord) -> list[str]:
    errors: list[str] = []
    if record.status not in REVIEW_STATUSES: errors.append("Invalid review status.")
    if record.disposition not in DISPOSITIONS: errors.append("Invalid review disposition.")
    if len(record.reviewer_reasoning) > 4000: errors.append("Reviewer reasoning exceeds the development limit.")
    if len(record.follow_up_notes) > 2000: errors.append("Follow-up notes exceed the development limit.")
    if record.follow_up_required and not record.follow_up_notes.strip(): errors.append("Follow-up notes are required when follow-up is selected.")
    return errors
