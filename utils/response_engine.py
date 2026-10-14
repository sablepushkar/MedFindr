"""Structured response pipeline for MedFindr, including bounded SignalGraph metadata."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from utils.analysis_trace import AnalysisTrace
from utils.clinical_data import ClinicalContext, extract_clinical_context
from utils.data_quality import DataQuality, assess_data_quality
from utils.drug_lookup import search_drug
from utils.ebm_risk import EBMExplanation, assess_risk_ebm
from utils.evidence import EvidenceItem, retrieved_evidence
from utils.safety_signals import SafetySignal, assess_safety_signal
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
    clinical_context: Optional[ClinicalContext] = None
    data_quality: Optional[DataQuality] = None
    safety_signal: Optional[SafetySignal] = None
    evidence: List[EvidenceItem] = field(default_factory=list)
    trace: Optional[AnalysisTrace] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "concern": self.concern,
            "urgency": self.urgency.to_dict(),
            "ebm": self.ebm.to_dict() if self.ebm else None,
            "sections": [
                {"title": s.title, "content": s.content, "level": s.level, "items": list(s.items)}
                for s in self.sections
            ],
            "drug_result": self.drug_result,
            "notes": self.notes,
            "errors": list(self.errors),
            "clinical_context": self.clinical_context.to_dict() if self.clinical_context else None,
            "data_quality": self.data_quality.to_dict() if self.data_quality else None,
            "safety_signal": self.safety_signal.to_dict() if self.safety_signal else None,
            "evidence": [item.to_dict() for item in self.evidence],
            "trace": self.trace.to_dict() if self.trace else None,
        }

def build_response(concern: str, drug_name: Optional[str] = None, include_ebm: bool = True) -> StructuredResponse:
    """Run a bounded, explainable workflow; generated flags are not clinical conclusions."""
    concern_validation = validate_concern(concern)
    if not concern_validation.valid:
        trace = AnalysisTrace()
        trace.add("validation", "failed", "Concern input rejected before analysis.")
        return StructuredResponse(
            concern="", urgency=assess_urgency(""),
            sections=[Section("1. Input Validation", concern_validation.error, "error")],
            notes="No analysis was performed because the concern input was invalid.",
            errors=[concern_validation.error], trace=trace,
        )

    cleaned = concern_validation.value
    drug_validation = validate_drug_name(drug_name) if drug_name else None
    cleaned_drug = drug_validation.value if drug_validation and drug_validation.valid else ""
    trace = AnalysisTrace()
    trace.add("validation", "passed", "Bounded and normalized input accepted.")

    context = extract_clinical_context(cleaned, cleaned_drug or None)
    trace.add("clinical_extraction", "completed", f"Extracted {len(context.symptoms)} supported symptom concept(s) and {len(context.medications)} medication context item(s).")
    quality = assess_data_quality(context, cleaned_drug or None)
    trace.add("data_quality", "completed", f"Prototype input completeness indicator: {quality.score}%.")
    urgency = assess_urgency(cleaned)
    trace.add("urgency", "completed", f"Rule-based informational flag: {urgency.level}.")
    signal = assess_safety_signal(context)
    trace.add("safety_signal", signal.status, signal.signal_type)
    ebm = assess_risk_ebm(cleaned, urgency_level=urgency.level) if include_ebm else None
    trace.add("ebm", "completed" if ebm else "skipped", "Experimental model layer evaluated." if ebm else "Experimental model layer disabled.")

    evidence = list(signal.evidence)
    sections = [
        Section("1. Understanding the Concern", cleaned),
        Section("2. Structured Findings", "The prototype converted selected phrases into a small normalized information model.", items=[
            f"Recognized symptom phrases: {', '.join(f.concept for f in context.symptoms) or 'none'}",
            f"Optional medication field: {cleaned_drug or 'not supplied'}",
            f"Stated medication timing phrase: {context.temporal_relationship}",
        ]),
        Section("3. Input Completeness", quality.label, items=[
            f"Prototype completeness indicator: {quality.score}% (not a clinical quality score)",
            f"Present: {', '.join(quality.present)}",
            f"Missing or unclear: {', '.join(quality.missing) or 'none in this limited model'}",
        ]),
        Section("4. Prototype Informational Flag", urgency.recommendation, urgency.level, list(urgency.reasons)),
        Section("5. Medication Safety Signal", signal.explanation, signal.priority if signal.priority in {"high", "moderate"} else None, [
            f"Signal: {signal.signal_type}", f"Status: {signal.status}", f"Review priority: {signal.priority}",
            f"Matched features: {', '.join(signal.matched_features) or 'none'}",
        ]),
    ]
    if ebm:
        factors = list(ebm.top_factors)
        factors.extend(f"{key}: {value:.2f}" for key, value in ebm.local_contribution.items())
        is_placeholder = ebm.model_status != "loaded"
        sections.append(Section(
            "6. Experimental Model Output (Fallback)" if is_placeholder else "6. Explainable Risk Assessment",
            f"{ebm.summary} {ebm.note}".strip() if is_placeholder else ebm.summary, ebm.risk_level, factors,
        ))
    sections.append(Section("7. General Information / Next Steps",
        "Prototype outputs should be reviewed as informational context rather than clinical conclusions.",
        items=[
            "Record relevant symptoms and how they change over time.",
            "Review medication timing and source information when relevant.",
            "Use a qualified clinician or pharmacist for individual medical advice.",
            "A detected phrase or signal does not establish diagnosis or causality.",
        ]))

    errors: list[str] = []
    drug_result: Optional[Dict[str, Any]] = None
    if drug_validation and not drug_validation.valid:
        errors.append(drug_validation.error)
        trace.add("external_retrieval", "rejected", "Drug lookup input failed validation.")
    elif drug_validation and drug_validation.value:
        drug_result = search_drug(drug_validation.value)
        trace.add("external_retrieval", drug_result.get("status", "unknown"), "OpenFDA label lookup completed.")
        if drug_result.get("status") == "success":
            evidence.append(retrieved_evidence(drug_result))

    notes = (
        "MedFindr is an actively developed healthcare/pharmaceutical information prototype. It organizes information and generates rule-based prototype flags; it is not a diagnostic system or autonomous clinical decision-maker. "
        "The phrase extraction and safety-signal layers are intentionally small, transparent pattern matchers and do not establish causality. "
        "The experimental model is used only when a compatible model artifact is available; otherwise a clearly labelled fallback is shown. "
        "Drug-label information is retrieved from OpenFDA and keeps source provenance with the result. Review records are session-scoped and exported on user request; they are not a compliance audit log."
    )
    return StructuredResponse(
        concern=cleaned, urgency=urgency, ebm=ebm, sections=sections, drug_result=drug_result,
        notes=notes, errors=errors, clinical_context=context, data_quality=quality,
        safety_signal=signal, evidence=evidence, trace=trace,
    )
