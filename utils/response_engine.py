"""Structured response and SignalGraph pipeline for MedFindr v1.2."""
from __future__ import annotations
import hashlib
from dataclasses import dataclass,field
from typing import Any,Dict,List,Optional
from utils.analysis_trace import AnalysisTrace
from utils.clinical_data import ClinicalContext,extract_clinical_context
from utils.data_quality import DataQuality,assess_data_quality
from utils.drug_lookup import search_drug
from utils.ebm_risk import EBMExplanation,assess_risk_ebm
from utils.evidence import EvidenceItem,retrieved_evidence
from utils.safety_signals import SafetySignal,assess_safety_signal
from utils.urgency import UrgencyResult,assess_urgency
from utils.validation import validate_concern,validate_drug_name
@dataclass
class Section:
    title:str
    content:str
    level:Optional[str]=None
    items:List[str]=field(default_factory=list)
@dataclass
class StructuredResponse:
    concern:str
    urgency:UrgencyResult
    ebm:Optional[EBMExplanation]=None
    sections:List[Section]=field(default_factory=list)
    drug_result:Optional[Dict[str,Any]]=None
    notes:str=""
    errors:List[str]=field(default_factory=list)
    clinical_context:Optional[ClinicalContext]=None
    data_quality:Optional[DataQuality]=None
    safety_signal:Optional[SafetySignal]=None
    evidence:List[EvidenceItem]=field(default_factory=list)
    trace:Optional[AnalysisTrace]=None
    def to_dict(self)->Dict[str,Any]:
        return {"concern":self.concern,"urgency":self.urgency.to_dict(),
                "ebm":self.ebm.to_dict() if self.ebm else None,
                "sections":[{"title":s.title,"content":s.content,"level":s.level,"items":s.items} for s in self.sections],
                "drug_result":self.drug_result,"notes":self.notes,"errors":self.errors,
                "clinical_context":self.clinical_context.to_dict() if self.clinical_context else None,
                "data_quality":self.data_quality.to_dict() if self.data_quality else None,
                "safety_signal":self.safety_signal.to_dict() if self.safety_signal else None,
                "evidence":[x.to_dict() for x in self.evidence],
                "trace":self.trace.to_dict() if self.trace else None}
def _analysis_id(concern:str,drug_name:str)->str:
    return "MF-"+hashlib.sha256(f"{concern}\n{drug_name}".encode()).hexdigest()[:12]
def build_response(concern:str,drug_name:Optional[str]=None,include_ebm:bool=True)->StructuredResponse:
    validation=validate_concern(concern)
    if not validation.valid:
        urgency=assess_urgency("")
        trace=AnalysisTrace(_analysis_id("","")); trace.add("validation","failed","Concern input rejected before analysis.")
        return StructuredResponse("",urgency,[ ] if False else None,
            [Section("1. Input Validation",validation.error,"error")],notes="No analysis was performed because the concern input was invalid.",
            errors=[validation.error],trace=trace)
    cleaned=validation.value
    drug_validation=validate_drug_name(drug_name) if drug_name else None
    cleaned_drug=drug_validation.value if drug_validation and drug_validation.valid else ""
    trace=AnalysisTrace(_analysis_id(cleaned,cleaned_drug)); trace.add("validation","passed","Bounded and normalized input accepted.")
    context=extract_clinical_context(cleaned,cleaned_drug or None)
    trace.add("clinical_extraction","completed",f"Extracted {len(context.symptoms)} supported symptom concept(s) and {len(context.medications)} medication context item(s).")
    quality=assess_data_quality(context,cleaned_drug or None); trace.add("data_quality","completed",f"Prototype input completeness: {quality.score}%.")
    urgency=assess_urgency(cleaned); trace.add("urgency","completed",f"Prototype urgency flag: {urgency.level}.")
    signal=assess_safety_signal(context); trace.add("safety_signal",signal.status,signal.signal_type)
    ebm=assess_risk_ebm(cleaned,urgency_level=urgency.level) if include_ebm else None
    trace.add("ebm","completed" if ebm else "skipped","Explainable risk layer evaluated." if ebm else "EBM layer disabled.")
    evidence=list(signal.evidence)
    sections=[
        Section("1. Understanding the Concern",cleaned),
        Section("2. Structured Findings","MedFindr converted the supplied text into a small normalized information model.",
                 items=[f"Symptoms detected: {', '.join(x.concept for x in context.symptoms) or 'none'}",
                        f"Medication context: {cleaned_drug or 'not supplied'}",
                        f"Temporal medication relationship: {context.temporal_relationship}"]),
        Section("3. Data Quality",quality.label,items=[f"Completeness indicator: {quality.score}%",
            f"Available: {', '.join(quality.present)}",f"Missing/unclear: {', '.join(quality.missing) or 'none in the prototype model'}"]),
        Section("4. Prototype Informational Flag",urgency.recommendation,urgency.level,list(urgency.reasons)),
        Section("5. Medication Safety Signal",signal.explanation,
                 signal.priority if signal.priority in {"high","moderate"} else None,
                 [f"Signal: {signal.signal_type}",f"Status: {signal.status}",f"Priority: {signal.priority}",
                  f"Matched features: {', '.join(signal.matched_features) or 'none'}"])]
    if ebm:
        factors=list(ebm.top_factors); factors.extend(f"{k}: {v:.2f}" for k,v in ebm.local_contribution.items())
        sections.append(Section("6. Explainable Risk Assessment",ebm.summary,ebm.risk_level,factors))
    sections.append(Section("7. General Information / Next Steps",
        "Prototype outputs should be reviewed as informational context rather than clinical conclusions.",
        items=["Record relevant symptoms and how they change over time.",
               "Review medication timing when evaluating a possible safety signal.",
               "Use a qualified clinician or pharmacist for individual medical advice.",
               "Treat all prototype flags as informational rather than clinical conclusions."]))
    errors=[]; drug_result=None
    if drug_validation and not drug_validation.valid:
        errors.append(drug_validation.error); trace.add("external_retrieval","rejected","Drug lookup input failed validation.")
    elif drug_validation and drug_validation.value:
        drug_result=search_drug(drug_validation.value)
        trace.add("external_retrieval",drug_result.get("status","unknown"),"OpenFDA label lookup completed.")
        if drug_result.get("status")=="success": evidence.append(retrieved_evidence(drug_result))
    else: trace.add("external_retrieval","skipped","No optional drug lookup requested.")
    notes=("MedFindr v1.2 introduces SignalGraph: a lightweight pipeline that converts supplied text into structured findings, "
           "prototype medication-related safety signals, evidence objects, data-quality indicators, and an analysis trace. "
           "These are software signals for information review, not diagnoses, causality assessments, treatment recommendations, "
           "or clinical validation. Retrieved label information remains separate from MedFindr-generated analysis.")
    return StructuredResponse(cleaned,urgency,ebm,sections,drug_result,notes,errors,context,quality,signal,evidence,trace)
