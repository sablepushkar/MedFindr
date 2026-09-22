"""Lightweight normalized clinical-information model for MedFindr v1.2."""
from __future__ import annotations
from dataclasses import dataclass,field
from typing import Any
@dataclass(frozen=True)
class ClinicalFinding:
    concept:str
    category:str
    matched_text:str
@dataclass(frozen=True)
class MedicationExposure:
    medication:str
    relationship:str
    matched_text:str
@dataclass
class ClinicalContext:
    concern:str
    symptoms:list[ClinicalFinding]=field(default_factory=list)
    medications:list[MedicationExposure]=field(default_factory=list)
    temporal_relationship:str="not_stated"
    context_terms:list[str]=field(default_factory=list)
    def to_dict(self)->dict[str,Any]:
        return {"concern":self.concern,"symptoms":[x.__dict__ for x in self.symptoms],
                "medications":[x.__dict__ for x in self.medications],
                "temporal_relationship":self.temporal_relationship,"context_terms":self.context_terms}
SYMPTOM_CONCEPTS={"severe headache":"neurological","shortness of breath":"respiratory",
"breathing difficulty":"respiratory","chest pain":"cardiac","unconsciousness":"neurological",
"fainting":"neurological","fever":"systemic","rash":"dermatologic","swelling":"general",
"headache":"neurological","dizziness":"neurological","vomiting":"gastrointestinal"}
def extract_clinical_context(concern:str,drug_name:str|None=None)->ClinicalContext:
    lower=concern.lower()
    symptoms=[ClinicalFinding(c,k,c) for c,k in sorted(SYMPTOM_CONCEPTS.items(),key=lambda x:-len(x[0])) if c in lower]
    exposure="not_stated"; matched=""
    for phrase in ("after taking","after starting","since taking","since starting","following medication","after medication","started the medicine"):
        if phrase in lower: exposure="after_medication_exposure"; matched=phrase; break
    medications=[MedicationExposure(drug_name,exposure,matched)] if drug_name else []
    context_terms=[x for x in ("after standing","after exercise","after eating","new medication","new medicine") if x in lower]
    return ClinicalContext(concern,symptoms,medications,exposure,context_terms)
