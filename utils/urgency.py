"""
Urgency and red-flag assessment module.
Version: 07.3 major

Transparent, rule-based engine.
Returns structured result that is easy to explain and audit.
No machine learning yet – deliberate design choice for clarity and safety.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class UrgencyResult:
    level: str                          # "high" | "moderate" | "low"
    score: int                          # simple internal score
    reasons: List[str] = field(default_factory=list)
    recommendation: str = ""

    def to_dict(self) -> dict:
        return {
            "level": self.level,
            "score": self.score,
            "reasons": self.reasons,
            "recommendation": self.recommendation,
        }


# High-priority red flag patterns (order does not matter)
HIGH_FLAGS = [
    ("chest pain", "Chest pain reported"),
    ("difficulty breathing", "Difficulty breathing / shortness of breath"),
    ("shortness of breath", "Shortness of breath"),
    ("severe chest", "Severe chest symptoms"),
    ("unconscious", "Loss of consciousness mentioned"),
    ("passed out", "Loss of consciousness mentioned"),
    ("sudden weakness", "Sudden weakness (possible neurological emergency)"),
    ("one side", "Symptoms affecting one side of the body"),
    ("stroke", "Stroke-related language used"),
    ("heart attack", "Heart attack-related language used"),
    ("severe bleeding", "Severe bleeding"),
    ("bleeding heavily", "Heavy bleeding"),
    ("coughing blood", "Coughing blood"),
    ("vomiting blood", "Vomiting blood"),
    ("suicidal", "Suicidal ideation language"),
    ("kill myself", "Suicidal ideation language"),
    ("severe headache with fever", "Severe headache associated with fever"),
    ("stiff neck with fever", "Stiff neck with fever (concerning combination)"),
    ("seizure", "Seizure mentioned"),
    ("worst headache", "Thunderclap / worst headache language"),
]

# Moderate concern patterns
MODERATE_FLAGS = [
    ("fever", "Fever present"),
    ("high fever", "High fever"),
    ("vomiting", "Vomiting"),
    ("unable to keep fluids", "Unable to keep fluids down"),
    ("dizziness", "Dizziness"),
    ("vertigo", "Vertigo / severe dizziness"),
    ("blood in urine", "Blood in urine"),
    ("blood in stool", "Blood in stool"),
    ("black stool", "Black stool"),
    ("burning sensation while urinating", "Dysuria (burning urination)"),
    ("painful urination", "Painful urination"),
    ("swelling", "Swelling reported"),
    ("rash with fever", "Rash associated with fever"),
    ("persistent vomiting", "Persistent vomiting"),
    ("dehydration", "Dehydration concern"),
    ("severe pain", "Severe pain"),
    ("uncontrolled pain", "Uncontrolled pain"),
    ("pregnancy", "Patient is pregnant – extra caution"),
    ("pregnant", "Patient is pregnant – extra caution"),
]


def assess_urgency(text: str) -> UrgencyResult:
    """
    Assess urgency from free-text concern.

    Returns a fully transparent UrgencyResult.
    Scoring is simple and explainable on purpose.
    """
    if not text or not text.strip():
        return UrgencyResult(
            level="low",
            score=0,
            reasons=["No concern text provided"],
            recommendation="Please describe the health concern.",
        )

    lower = text.lower().strip()
    score = 0
    reasons: List[str] = []

    # Check high flags first
    for pattern, reason in HIGH_FLAGS:
        if pattern in lower:
            score += 10
            if reason not in reasons:
                reasons.append(reason)

    # Then moderate flags
    for pattern, reason in MODERATE_FLAGS:
        if pattern in lower:
            score += 3
            if reason not in reasons:
                reasons.append(reason)

    # Determine level
    if score >= 10:
        level = "high"
        recommendation = (
            "High urgency signals detected. "
            "If the symptoms are currently present and severe, seek emergency medical care immediately."
        )
    elif score >= 3:
        level = "moderate"
        recommendation = (
            "Moderate concern indicators present. "
            "Monitor closely. Seek medical review promptly if symptoms worsen, persist, or new concerning signs appear."
        )
    else:
        level = "low"
        recommendation = (
            "No strong red-flag patterns detected on the current description. "
            "Continue to monitor. Seek care if symptoms change or do not improve."
        )

    if not reasons:
        reasons.append("No specific red-flag keywords matched")

    return UrgencyResult(
        level=level,
        score=score,
        reasons=reasons,
        recommendation=recommendation,
    )
