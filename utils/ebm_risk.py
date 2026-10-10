"""Explainable Boosting Machine risk module with cached model loading and transparent fallback."""
from __future__ import annotations
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List
from config import EBM_MODEL_PATH
logger=logging.getLogger(__name__)
_model_cache: dict[str, Any] = {}
@dataclass
class EBMExplanation:
    risk_level:str; risk_score:float; summary:str
    top_factors:List[str]=field(default_factory=list)
    local_contribution:Dict[str,float]=field(default_factory=dict)
    model_status:str="placeholder"; note:str=""
    def to_dict(self)->Dict[str,Any]:
        return {"risk_level":self.risk_level,"risk_score":round(self.risk_score,3),"summary":self.summary,"top_factors":self.top_factors,"local_contribution":{k:round(v,3) for k,v in self.local_contribution.items()},"model_status":self.model_status,"note":self.note}
def _placeholder_assess(urgency_level:str)->EBMExplanation:
    if urgency_level=="high": return EBMExplanation("high",0.84,"Elevated risk signals detected by the prototype rule layer.",["High-priority urgency pattern matched","Language indicating potential severity"],{"high_urgency_keywords":0.58,"severity_language":0.26},"placeholder","Placeholder only. Run scripts/train_ebm.py to create a trained model.")
    if urgency_level=="moderate": return EBMExplanation("moderate",0.47,"Moderate concern indicators detected by the prototype rule layer.",["Moderate concern pattern matched","No high-priority rule was matched"],{"moderate_keywords":0.33,"contextual_signals":0.14},"placeholder","Placeholder only. Run scripts/train_ebm.py to create a trained model.")
    return EBMExplanation("low",0.16,"No strong concern pattern was detected by the prototype rule layer.",["No high-priority or moderate concern pattern matched"],{"baseline":0.16},"placeholder","Placeholder only. Run scripts/train_ebm.py to create a trained model.")
def load_ebm_model(model_path: Path = EBM_MODEL_PATH):
    """Load each configured model path at most once per process."""
    key = str(Path(model_path).expanduser().resolve())
    if key in _model_cache:
        return _model_cache[key]
    if not Path(key).exists():
        return None
    try:
        import joblib
        model = joblib.load(key)
    except Exception as exc:
        logger.warning("Could not load EBM model from %s: %s", key, exc)
        return None
    logger.info("EBM model loaded from %s", key)
    _model_cache[key] = model
    return model
def extract_features(text:str)->Dict[str,int]:
    t=(text or "").lower()
    return {"has_chest_pain":int("chest pain" in t or "chest" in t),"has_breathing":int("breath" in t or "dyspnea" in t or "shortness" in t),"has_fever":int("fever" in t),"has_severe":int("severe" in t or "worst" in t or "intense" in t),"has_neuro":int("weakness" in t or "stroke" in t or "one side" in t or "numb" in t),"has_bleeding":int("bleed" in t or "blood" in t),"has_vomit":int("vomit" in t),"has_dizziness":int("dizzy" in t or "dizziness" in t or "vertigo" in t),"duration_days":3,"text_length":min(len(t.split()),50)}
def assess_risk_ebm(concern:str,urgency_level:str="low",model=None)->EBMExplanation:
    if model is None: model=load_ebm_model()
    if model is not None:
        try:
            import pandas as pd
            frame=pd.DataFrame([extract_features(concern)]); prediction=model.predict(frame)[0]; probabilities=model.predict_proba(frame)[0]
            risk_level={0:"low",1:"moderate",2:"high"}.get(int(prediction),"low")
            return EBMExplanation(risk_level,float(max(probabilities)),f"EBM model assessment: {risk_level} risk.",["Prediction from trained Explainable Boosting Machine"],{},"loaded","Result from the trained EBM model.")
        except Exception as exc: logger.warning("Model prediction failed (%s). Falling back to placeholder.",exc)
    return _placeholder_assess(urgency_level)
