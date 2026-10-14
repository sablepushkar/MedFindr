"""Medication-related safety-signal pattern detection for MedFindr v1.2.
This module flags information patterns for review. It does not infer causality.
"""
from __future__ import annotations
from dataclasses import dataclass,field
from typing import Any
from utils.clinical_data import ClinicalContext
from utils.evidence import EvidenceItem,rule_evidence
@dataclass
class SafetySignal:
    signal_type:str
    priority:str
    status:str
    matched_features:list[str]=field(default_factory=list)
    explanation:str=""
    evidence:list[EvidenceItem]=field(default_factory=list)
    def to_dict(self)->dict[str,Any]:
        return {"signal_type":self.signal_type,"priority":self.priority,"status":self.status,
                "matched_features":list(self.matched_features),"explanation":self.explanation,
                "evidence":[x.to_dict() for x in self.evidence]}
def assess_safety_signal(context:ClinicalContext)->SafetySignal:
    if not context.medications:
        return SafetySignal("no medication exposure supplied","none","not_assessed",
            explanation="No medication was supplied, so the medication-related signal layer was not assessed.")
    medication=context.medications[0]
    symptoms=[x.concept for x in context.symptoms]
    if medication.relationship=="after_medication_exposure" and symptoms:
        priority="high" if any(x in {"breathing difficulty","shortness of breath","fainting","unconsciousness"} for x in symptoms) else "review"
        return SafetySignal("potential medication-related safety signal",priority,"flagged",
            ["medication supplied","symptom concepts detected","temporal relationship stated after medication exposure"],
            "The supplied information contains a medication exposure, symptoms, and a stated temporal relationship. "
            "This is a prototype signal for review, not evidence of causality.",
            [rule_evidence("Medication-exposure pattern",
                "Medication exposure and reported symptoms occur with a stated temporal relationship.",
                "medication_exposure_with_symptoms")])
    if symptoms:
        return SafetySignal("medication mentioned; temporal relationship unclear","review","context_incomplete",
            ["medication supplied","symptom concepts detected"],
            "A medication and symptom information were supplied, but the temporal relationship is not stated clearly enough "
            "for the prototype to flag an exposure pattern.",
            [rule_evidence("Incomplete medication context",
                "Medication and symptoms are present without a stated exposure sequence.",
                "medication_context_incomplete")])
    return SafetySignal("insufficient symptom context","none","insufficient_context",
        ["medication supplied"],"A medication was supplied, but no supported symptom concept was extracted.")
