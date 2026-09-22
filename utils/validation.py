"""Input validation and normalization for the MedFindr prototype."""

from __future__ import annotations

import re
from dataclasses import dataclass

MAX_CONCERN_LENGTH = 2000
MAX_DRUG_NAME_LENGTH = 120
_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


@dataclass(frozen=True)
class ValidationResult:
    value: str
    error: str = ""

    @property
    def valid(self) -> bool:
        return not self.error


def _clean(value: object) -> str:
    text = str(value or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    return _CONTROL_CHARS.sub("", text)


def validate_concern(value: object) -> ValidationResult:
    text = _clean(value)
    if not text:
        return ValidationResult("", "Please enter a health concern.")
    if len(text) > MAX_CONCERN_LENGTH:
        return ValidationResult("", f"Health concern is too long. Keep it under {MAX_CONCERN_LENGTH} characters.")
    return ValidationResult(text)


def validate_drug_name(value: object) -> ValidationResult:
    text = _clean(value)
    if not text:
        return ValidationResult("")
    if len(text) > MAX_DRUG_NAME_LENGTH:
        return ValidationResult("", f"Drug name is too long. Keep it under {MAX_DRUG_NAME_LENGTH} characters.")
    return ValidationResult(text)
