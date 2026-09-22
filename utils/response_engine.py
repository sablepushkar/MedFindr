"""Structured Response Engine with separated urgency, EBM, and drug lookup layers."""
from __future__ import annotations
from dataclasses import dataclass,field
from typing import Any,Dict,List,Optional
from utils.drug_lookup import search_drug
from utils.ebm_risk import EBMExplanation,assess_risk_ebm
from utils.urgency import UrgencyResult,assess_urgency
@dataclass
class Section:
    title:str; content:str; level:Optional[str]=None; items:List[str]=field(default_factory=list)
@dataclass
class StructuredResponse:
    concern:str; urgency:UrgencyResult; ebm:Optional[EBMExplanation]=None; sections:List[Section]=field(default_factory=list); drug_result:Optional[Dict[str,Any]]=None; notes:str=""
    def to_dict(self)->Dict[str,Any]: return {"concern":self.concern,"urgency":self.urgency.to_dict(),"ebm":self.ebm.to_dict() if self.ebm else None,"sections":[{"title":s.title,"content":s.content,"level":s.level,"items":s.items} for s in self.sections],"drug_result":self.drug_result,"notes":self.notes}
def build_response(concern:str,drug_name:Optional[str]=None,include_ebm:bool=True)->StructuredResponse:
    cleaned=(concern or "").strip(); urgency=assess_urgency(cleaned)
    ebm=assess_risk_ebm(cleaned,urgency_level=urgency.level) if include_ebm else None
    sections=[Section("1. Understanding the Concern",cleaned if cleaned else "No concern text provided."),Section("2. Urgency Assessment (Rule-based)",urgency.recommendation,urgency.level,list(urgency.reasons))]
    if ebm:
        factors=list(ebm.top_factors); factors.extend(f"{k}: {v:.2f}" for k,v in ebm.local_contribution.items()); sections.append(Section("3. Explainable Risk Assessment (EBM)",ebm.summary,ebm.risk_level,factors))
    if urgency.level=="high": next_content="High-priority signals matched. Urgent medical evaluation should be considered."
    elif urgency.level=="moderate": next_content="Moderate concern indicators matched. Timely medical review may be appropriate if symptoms persist or worsen."
    else: next_content="No strong red-flag pattern matched this description. Continue monitoring and seek care if the situation changes."
    sections.append(Section("4. Possible Next Steps / General Information",next_content,["Record relevant symptoms and how they change over time.","Monitor for worsening or new concerning symptoms.","Use a qualified clinician or pharmacist for individual medical advice.","Seek urgent care when severe or rapidly worsening symptoms occur."]))
    drug_result=search_drug(drug_name.strip()) if drug_name and drug_name.strip() else None
    notes=("MedFindr is a portfolio prototype, not a clinical decision system. Urgency is a transparent rule-based classification. The EBM layer uses a trained model only when one is available; otherwise it exposes a clearly labelled placeholder. Drug information is sourced from the configured OpenFDA label endpoint.")
    return StructuredResponse(cleaned,urgency,ebm,sections,drug_result,notes)
