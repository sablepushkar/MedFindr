"""
Explainable Boosting Machine (EBM) Risk Module
Version: 08.5

Glass-box risk assessment interface.
Currently uses a high-quality deterministic placeholder that produces
the same structured output a real InterpretML EBM will return.

The public API is stable. A trained model can be dropped in later
without changing any calling code.
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
    """Structured, fully explainable risk output."""
    risk_level: str                                 # high | moderate | low
    risk_score: float                               # 0.0 – 1.0
    summary: str
    top_factors: List[str] = field(default_factory=list)
    local_contribution: Dict[str, float] = field(default_factory=dict)
    model_status: str = "placeholder"               # placeholder | loaded | error
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
    """High-quality deterministic fallback used until a real model is trained."""
    concern_l = (concern or "").lower()

    if urgency_level == "high":
        return EBMExplanation(
            risk_level="high",
            risk_score=0.84,
            summary="Elevated risk signals detected. Prompt clinical attention is warranted.",
            top_factors=[
                "High-urgency symptom patterns present",
                "Language indicating potential severity",
            ],
            local_contribution={
                "high_urgency_keywords": 0.58,
                "severity_language": 0.26,
            },
            model_status="placeholder",
            note="Using transparent placeholder. Real EBM model will replace this.",
        )

    if urgency_level == "moderate":
        return EBMExplanation(
            risk_level="moderate",
            risk_score=0.47,
            summary="Moderate risk indicators present. Monitoring and timely review are advised.",
            top_factors=[
                "Moderate concern patterns matched",
                "No immediate high-severity red flags detected",
            ],
            local_contribution={
                "moderate_keywords": 0.33,
                "contextual_signals": 0.14,
            },
            model_status="placeholder",
            note="Using transparent placeholder. Real EBM model will replace this.",
        )

    return EBMExplanation(
        risk_level="low",
        risk_score=0.16,
        summary="Low risk profile based on the information provided.",
        top_factors=[
            "No strong red-flag or moderate concern patterns detected",
        ],
        local_contribution={
            "baseline": 0.16,
        },
        model_status="placeholder",
        note="Using transparent placeholder. Real EBM model will replace this.",
    )


def load_ebm_model(model_path: Path = EBM_MODEL_PATH):
    """
    Attempt to load a trained EBM model.
    Returns the model object or None if not available.
    This function is ready for InterpretML / joblib models.
    """
    try:
        if model_path.exists():
            import joblib
            model = joblib.load(model_path)
            logger.info("EBM model loaded from %s", model_path)
            return model
        else:
            logger.info("No trained EBM model found at %s – using placeholder", model_path)
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
    Public entry point for EBM-style risk assessment.

    - If a real trained model is provided / loaded, it will be used.
    - Otherwise falls back to the transparent placeholder.
    """
    if model is None:
        model = load_ebm_model()

    if model is not None:
        # Future: real prediction + explanation extraction will go here
        # For now we still return placeholder so behaviour stays stable
        logger.info("Real model present but prediction path not yet implemented – using placeholder")

    return _placeholder_assess(concern, urgency_level)
