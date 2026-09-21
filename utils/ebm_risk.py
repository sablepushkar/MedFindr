"""
Explainable Boosting Machine (EBM) Risk Module
Version: V09.1a

Supports both:
- A trained InterpretML EBM model (when available)
- A high-quality transparent placeholder (safe fallback)
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
    """Safe deterministic fallback."""
    if urgency_level == "high":
        return EBMExplanation(
            risk_level="high",
            risk_score=0.84,
            summary="Elevated risk signals detected. Prompt clinical attention is warranted.",
            top_factors=["High-urgency symptom patterns present", "Language indicating potential severity"],
            local_contribution={"high_urgency_keywords": 0.58, "severity_language": 0.26},
            model_status="placeholder",
            note="Using transparent placeholder. Train a real EBM with scripts/train_ebm.py",
        )
    if urgency_level == "moderate":
        return EBMExplanation(
            risk_level="moderate",
            risk_score=0.47,
            summary="Moderate risk indicators present. Monitoring and timely review are advised.",
            top_factors=["Moderate concern patterns matched", "No immediate high-severity red flags detected"],
            local_contribution={"moderate_keywords": 0.33, "contextual_signals": 0.14},
            model_status="placeholder",
            note="Using transparent placeholder. Train a real EBM with scripts/train_ebm.py",
        )
    return EBMExplanation(
        risk_level="low",
        risk_score=0.16,
        summary="Low risk profile based on the information provided.",
        top_factors=["No strong red-flag or moderate concern patterns detected"],
        local_contribution={"baseline": 0.16},
        model_status="placeholder",
        note="Using transparent placeholder. Train a real EBM with scripts/train_ebm.py",
    )


def load_ebm_model(model_path: Path = EBM_MODEL_PATH):
    """Load a trained EBM model if it exists."""
    try:
        if model_path.exists():
            import joblib
            model = joblib.load(model_path)
            logger.info("EBM model loaded successfully from %s", model_path)
            return model
        logger.info("No trained model found at %s – using placeholder", model_path)
        return None
    except Exception as exc:
        logger.warning("Failed to load EBM model: %s", exc)
        return None


def assess_risk_ebm(
    concern: str,
    urgency_level: str = "low",
    model=None,
) -> EBMExplanation:
    """
    Main entry point.
    Tries to use a real trained model; falls back to placeholder.
    """
    if model is None:
        model = load_ebm_model()

    if model is not None:
        try:
            # Very simple feature extraction for the first real model
            # (This will be improved in later versions)
            text = (concern or "").lower()
            features = {
                "has_chest_pain": int("chest pain" in text or "chest" in text),
                "has_breathing": int("breath" in text or "dyspnea" in text),
                "has_fever": int("fever" in text),
                "has_severe": int("severe" in text or "worst" in text),
                "has_neuro": int("weakness" in text or "stroke" in text or "one side" in text),
                "has_bleeding": int("bleed" in text or "blood" in text),
                "text_length": min(len(text.split()), 50),
            }

            import pandas as pd
            X = pd.DataFrame([features])

            # Predict
            pred = model.predict(X)[0]
            proba = model.predict_proba(X)[0]

            # Map prediction to risk level
            label_map = {0: "low", 1: "moderate", 2: "high"}
            risk_level = label_map.get(int(pred), "low")
            risk_score = float(max(proba))

            # Try to get local explanation if the model supports it
            top_factors = []
            local_contrib = {}
            try:
                explanation = model.explain_local(X)
                # Basic extraction – will be refined later
                top_factors = ["Model-based factors (see local explanation)"]
            except Exception:
                top_factors = ["Trained EBM prediction"]

            return EBMExplanation(
                risk_level=risk_level,
                risk_score=risk_score,
                summary=f"EBM model prediction: {risk_level} risk.",
                top_factors=top_factors,
                local_contribution=local_contrib,
                model_status="loaded",
                note="Prediction from trained Explainable Boosting Machine.",
            )
        except Exception as exc:
            logger.warning("Real model prediction failed: %s – falling back to placeholder", exp)

    return _placeholder_assess(concern, urgency_level)
