"""Small, transparent clinical-information extraction for the MedFindr prototype.

This is a phrase matcher, not a clinical NLP model. It deliberately reports only
recognized text patterns and does not infer diagnoses or medication causality.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class ClinicalFinding:
    concept: str
    category: str
    matched_text: str

@dataclass(frozen=True)
class MedicationExposure:
    medication: str
    relationship: str
    matched_text: str

@dataclass
class ClinicalContext:
    concern: str
    symptoms: list[ClinicalFinding] = field(default_factory=list)
    medications: list[MedicationExposure] = field(default_factory=list)
    temporal_relationship: str = "not_stated"
    context_terms: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "concern": self.concern,
            "symptoms": [x.__dict__ for x in self.symptoms],
            "medications": [x.__dict__ for x in self.medications],
            "temporal_relationship": self.temporal_relationship,
            "context_terms": list(self.context_terms),
        }

SYMPTOM_CONCEPTS = {
    "shortness of breath": "respiratory",
    "difficulty breathing": "respiratory",
    "breathing difficulty": "respiratory",
    "cannot breathe": "respiratory",
    "can't breathe": "respiratory",
    "unable to breathe": "respiratory",
    "severe headache": "neurological",
    "chest tightness": "cardiac",
    "chest pain": "cardiac",
    "unconsciousness": "neurological",
    "fainting": "neurological",
    "vomiting": "gastrointestinal",
    "swelling": "general",
    "dizziness": "neurological",
    "headache": "neurological",
    "fever": "systemic",
    "rash": "dermatologic",
}
_NEGATION = re.compile(
    r"(?:\bno\b|\bdenies\b|\bdenied\b|\bwithout\b|\bnot\b|\bnever\b|"
    r"\babsence of\b|\bnegative for\b|\bfree of\b|\bdoes not have\b|"
    r"\bdoesn't have\b|\bnot experiencing\b)"
    r"(?:\s+(?!and\b|or\b|but\b|however\b|while\b|although\b|yet\b|except\b)[\w'-]+){0,3}\s*$",
    re.IGNORECASE,
)

def is_negated_phrase(text: str, start: int) -> bool:
    """Return whether a recognized phrase has a nearby direct negation prefix."""
    window = text[max(0, start - 55):start]
    return bool(_NEGATION.search(window))

def _extract_symptoms(text: str) -> list[ClinicalFinding]:
    candidates: list[tuple[int, int, str, str, str]] = []
    for concept, category in sorted(SYMPTOM_CONCEPTS.items(), key=lambda item: len(item[0]), reverse=True):
        for match in re.finditer(re.escape(concept), text, flags=re.IGNORECASE):
            if is_negated_phrase(text, match.start()):
                continue
            if any(match.start() < end and match.end() > start for start, end, *_ in candidates):
                continue
            candidates.append((match.start(), match.end(), concept, category, match.group(0)))
    candidates.sort(key=lambda item: item[0])
    return [ClinicalFinding(concept, category, matched) for _, _, concept, category, matched in candidates]

def extract_clinical_context(concern: str, drug_name: str | None = None) -> ClinicalContext:
    text = str(concern or "")
    lower = text.lower()
    symptoms = _extract_symptoms(text)
    exposure_phrases = (
        "after taking", "after starting", "since taking", "since starting",
        "following medication", "after medication", "started the medicine",
        "after taking the medicine", "after taking the medication",
    )
    matched = next((phrase for phrase in exposure_phrases if phrase in lower), "")
    relationship = "after_medication_exposure" if matched else "not_stated"
    medications = [MedicationExposure(str(drug_name), relationship, matched)] if drug_name else []
    context_terms = [term for term in ("after standing", "after exercise", "after eating", "new medication", "new medicine") if term in lower]
    return ClinicalContext(text, symptoms, medications, relationship, context_terms)
