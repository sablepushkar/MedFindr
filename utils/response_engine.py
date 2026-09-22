"""Structured response pipeline for MedFindr."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from utils.drug_lookup import search_drug
from utils.ebm_risk import EBMExplanation, assess_risk_ebm
from utils.urgency import UrgencyResult, assess_urgency
from utils.validation import validate_concern, validate_drug_name


@dataclass
class Section:
    title: str
    content: str
    level: Optional[str] = None
    items: List[str] = field(default_factory=list)


@dataclass
class StructuredResponse:
    concern: str
    urgency: UrgencyResult
    ebm: Optional[EBMExplanation] = None
    sections: List[Section] = field(default_factory=list)
    drug_result: Optional[Dict[str, Any]] = None
    notes: str = ""
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "concern": self.concern,
            "urgency": self.urgency.to_dict(),
            "ebm": self.ebm.to_dict() if self.ebm else None,
            "sections": [
                {
                    "title": section.title,
                    "content": section.content,
                    "level": section.level,
                    "items": section.items,
                }
                for section in self.sections
            ],
            "drug_result": self.drug_result,
            "notes": self.notes,
            "errors": self.errors,
        }


def build_response(
    concern: str,
    drug_name: Optional[str] = None,
    include_ebm: bool = True,
) -> StructuredResponse:
    concern_validation = validate_concern(concern)
    if not concern_validation.valid:
        urgency = assess_urgency("")
        return StructuredResponse(
            concern="",
            urgency=urgency,
            sections=[
                Section(
                    "1. Input Validation",
                    concern_validation.error,
                    "error",
                )
            ],
            notes="No analysis was performed because the concern input was invalid.",
            errors=[concern_validation.error],
        )

    cleaned = concern_validation.value
    urgency = assess_urgency(cleaned)
    ebm = assess_risk_ebm(cleaned, urgency_level=urgency.level) if include_ebm else None

    sections = [
        Section("1. Understanding the Concern", cleaned),
        Section(
            "2. Prototype Informational Flag",
            urgency.recommendation,
            urgency.level,
            list(urgency.reasons),
        ),
    ]

    if ebm:
        factors = list(ebm.top_factors)
        factors.extend(
            f"{key}: {value:.2f}"
            for key, value in ebm.local_contribution.items()
        )
        sections.append(
            Section(
                "3. Explainable Risk Assessment",
                ebm.summary,
                ebm.risk_level,
                factors,
            )
        )

    next_content = (
        "High-priority prototype signals matched. Seek appropriate professional "
        "medical evaluation, particularly if symptoms are severe or worsening."
        if urgency.level == "high"
        else "Moderate prototype indicators matched. Consider professional medical "
        "review if symptoms persist, worsen, or new concerning signs appear."
        if urgency.level == "moderate"
        else "No strong red-flag pattern matched this description. Continue monitoring "
        "and seek professional care if the situation changes or does not improve."
    )

    sections.append(
        Section(
            "4. General Information / Next Steps",
            next_content,
            None,
            [
                "Record relevant symptoms and how they change over time.",
                "Monitor for worsening or new concerning symptoms.",
                "Use a qualified clinician or pharmacist for individual medical advice.",
                "Treat all prototype flags as informational rather than clinical conclusions.",
            ],
        )
    )

    errors: list[str] = []
    drug_result = None
    if drug_name:
        drug_validation = validate_drug_name(drug_name)
        if not drug_validation.valid:
            errors.append(drug_validation.error)
            sections.append(Section("5. Drug Information", drug_validation.error, "error"))
        elif drug_validation.value:
            drug_result = search_drug(drug_validation.value)
        else:
            drug_result = None

    notes = (
        "MedFindr is an actively developed healthcare/pharmaceutical technology "
        "prototype. It organizes information and generates prototype informational "
        "flags; it is not a diagnostic system or autonomous clinical decision-maker. "
        "The urgency layer is rule-based. The EBM layer uses a trained model only "
        "when a compatible model artifact is available; otherwise it exposes a "
        "clearly labelled fallback. Drug information is retrieved from OpenFDA and "
        "keeps source provenance with the result."
    )

    return StructuredResponse(
        cleaned,
        urgency,
        ebm,
        sections,
        drug_result,
        notes,
        errors,
    )
