"""
Explainable Boosting Machine (EBM) Risk Module
Version: X1.0+

Loads a trained model when available, otherwise uses a transparent placeholder.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from config import EBM_MODEL_PATH

logger = logging.getLogger(__name__)


@dataclass
class EBMExplanation:
    risk_level: str
    risk_score: float
    summary: str
    top_factors: List[str] = field(default_factory=list)
    local_contribution: Dict[str, float] = field(default_factory=dict)
    model_status: str = "placeholder"
    note: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "risk_level": self.risk_level,
            "risk_score": round(self.risk_score, 3),
            "summary": self.summary,
            "top_factors": self.top_factors,
            "local_contribution": {k: round(v, 3) for k, v in self.local_contribution.items()},
            "model_status": self.model_status,
            "note": self.note,
        }


def _placeholder_assess(concern: str, urgency_level: str) -> EBMExplanation:
    if urgency_level == "high":
        return EBMExplanation(
            risk_level="high",
            risk_score=0.84,
            summary="Elevated risk signals detected. Prompt clinical attention is warranted.",
            top_factors=["High-urgency symptom patterns present", "Language indicating potential severity"],
            local_contribution={"high_urgency_keywords": 0.58, "severity_language": 0.26},
            model_status="placeholder",
            note="Using transparent placeholder. Run scripts/train_ebm.py to create a real model.",
        )
    if urgency_level == "moderate":
        return EBMExplanation(
            risk_level="moderate",
            risk_score=0.47,
            summary="Moderate risk indicators present. Monitoring and timely review are advised.",
            top_factors=["Moderate concern patterns matched", "No immediate high-severity red flags"],
            local_contribution={"moderate_keywords": 0.33, "contextual_signals": 0.14},
            model_status="placeholder",
            note="Using transparent placeholder. Run scripts/train_ebm.py to create a real model.",
        )
    return EBMExplanation(
        risk_level="low",
        risk_score=0.16,
        summary="Low risk profile based on the information provided.",
        top_factors=["No strong red-flag or moderate concern patterns detected"],
        local_contribution={"baseline": 0.16},
        model_status="placeholder",
        note="Using transparent placeholder. Run scripts/train_ebm.py to create a real model.",
    )


def load_ebm_model(model_path: Path = EBM_MODEL_PATH):
    try:
        if model_path.exists():
            import joblib
            model = joblib.load(model_path)
            logger.info("EBM model loaded from %s", model_path)
            return model
        return None
    except Exception as exc:
        logger.warning("Could not load EBM model: %s", exc)
        return None


def extract_features(text: str) -> Dict[str, int]:
    """Simple but improved feature extraction used by the trained model."""
    t = (text or "").lower()
    return {
        "has_chest_pain": int("chest pain" in t or "chest" in t),
        "has_breathing": int("breath" in t or "dyspnea" in t or "shortness" in t),
        "has_fever": int("fever" in t),
        "has_severe": int("severe" in t or "worst" in t or "intense" in t),
        "has_neuro": int("weakness" in t or "stroke" in t or "one side" in t or "numb" in t),
        "has_bleeding": int("bleed" in t or "blood" in t),
        "has_vomit": int("vomit" in t or "vomiting" in t),
        "has_dizziness": int("dizzy" in t or "dizziness" in t or "vertigo" in t),
        "duration_days": 3,  # default when not specified
        "text_length": min(len(t.split()), 50),
    }


def assess_risk_ebm(
    concern: str,
    urgency_level: str = "low",
    model=None,
) -> EBMExplanation:
    if model is None:
        model = load_ebm_model()

    if model is not None:
        try:
            import pandas as pd
            features = extract_features(concern)
            X = pd.DataFrame([features])

            pred = model.predict(X)[0]
            proba = model.predict_proba(X)[0]

            label_map = {0: "low", 1: "moderate", 2: "high"}
            risk_level = label_map.get(int(pred), "low")
            risk_score = float(max(proba))

            return EBMExplanation(
                risk_level=risk_level,
                risk_score=risk_score,
                summary=f"EBM model assessment: {risk_level} risk.",
                top_factors=["Prediction from trained Explainable Boosting Machine"],
                local_contribution={},
                model_status="loaded",
                note="Result from trained EBM model.",
            )
        except Exception as exc:
            logger.warning("Model prediction failed (%s). Falling back to placeholder.", exc)

    return _placeholder_assess(concern, urgency_level)
