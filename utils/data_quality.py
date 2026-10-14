"""Input completeness checks for MedFindr v1.2."""
from __future__ import annotations
from dataclasses import dataclass,field
from typing import Any
from utils.clinical_data import ClinicalContext
@dataclass
class DataQuality:
    score:int
    label:str
    present:list[str]=field(default_factory=list)
    missing:list[str]=field(default_factory=list)
    def to_dict(self)->dict[str,Any]:
        return {"score":self.score,"label":self.label,"present":list(self.present),"missing":list(self.missing)}
def assess_data_quality(context:ClinicalContext,drug_name:str|None)->DataQuality:
    present=["concern"]; missing=[]
    if context.symptoms: present.append("recognizable symptom concepts")
    else: missing.append("recognizable symptom concepts")
    if drug_name: present.append("medication/lookup term")
    else: missing.append("medication/lookup term")
    if context.temporal_relationship!="not_stated": present.append("temporal medication relationship")
    else: missing.append("temporal medication relationship")
    if context.context_terms: present.append("context")
    else: missing.append("context")
    score=round(len(present)/5*100)
    label="Good prototype input completeness" if score>=80 else "Partial prototype input" if score>=50 else "Limited prototype input"
    return DataQuality(score,label,present,missing)
