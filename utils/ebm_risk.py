"""
Explainable Boosting Machine (EBM) Risk Module
Version: 08.1 Beta testing EBM

This module provides the interface for glass-box risk assessment.
Currently contains a clean placeholder + structured output so the
rest of the system can already consume EBM-style results.

Real model training and loading will be added in the next iteration.
Design goal: full explainability (global + local) while staying simple.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class EBMExplanation:
    """Structured explanation from an EBM-style model."""
    risk_level: str                          # "high" | "moderate" | "low"
    risk_score: float                        # 0.0 – 1.0
    summary: str
    top_factors: List[str] = field(default_factory=list)
    local_contribution: Dict[str, float] = field(default_factory=dict)
    note: str = "EBM model not yet trained – using transparent rule-based fallback."

    def to_dict(self) -> Dict[str, Any]:
        return {
            "risk_level": self.risk_level,
            "risk_score": self.risk_score,
            "summary": self.summary,
            "top_factors": self.top_factors,
            "local_contribution": self.local_contribution,
            "note": self.note,
        }


def assess_risk_ebm(concern: str, urgency_level: str = "low") -> EBMExplanation:
    """
    Placeholder EBM risk assessment.

    In this beta version we return a structured, explainable result
    that mirrors what a real InterpretML EBM would produce.
    This keeps the pipeline ready for a trained model without
    breaking current behaviour.
    """
    cleaned = (concern or "").strip().lower()

    # Simple deterministic mapping so the interface is already testable
    if urgency_level == "high":
        return EBMExplanation(
            risk_level="high",
            risk_score=0.82,
            summary="Elevated risk signals detected from the current description.",
            top_factors=[
                "Presence of high-urgency keywords",
                "Symptom combination requires prompt attention",
            ],
            local_contribution={
                "urgency_keywords": 0.55,
                "symptom_severity_language": 0.27,
            },
            note="Beta placeholder – real EBM model will replace this logic.",
        )

    if urgency_level == "moderate":
        return EBMExplanation(
            risk_level="moderate",
            risk_score=0.48,
            summary="Moderate risk indicators present. Monitoring and timely review advised.",
            top_factors=[
                "Moderate concern patterns matched",
                "No immediate high-severity red flags",
            ],
            local_contribution={
                "moderate_keywords": 0.31,
                "duration_language": 0.17,
            },
            note="Beta placeholder – real EBM model will replace this logic.",
        )

    # Default low
    return EBMExplanation(
        risk_level="low",
        risk_score=0.18,
        summary="Low risk profile based on the current description.",
        top_factors=[
            "No strong red-flag or moderate concern patterns detected",
        ],
        local_contribution={
            "baseline": 0.18,
        },
        note="Beta placeholder – real EBM model will replace this logic.",
    )
