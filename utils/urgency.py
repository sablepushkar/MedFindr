"""Urgency and red-flag assessment module.

Transparent rule-based prototype classification layer; not a clinical diagnostic or triage system.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass
class UrgencyResult:
    level: str
    score: int
    reasons: List[str] = field(default_factory=list)
    recommendation: str = ""
    def to_dict(self) -> dict:
        return {"level": self.level, "score": self.score, "reasons": self.reasons, "recommendation": self.recommendation}

HIGH_FLAGS: List[Tuple[str, str]] = [
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
    ("severe headache with fever", "Severe headache associated with fever"),
    ("stiff neck with fever", "Stiff neck with fever (concerning combination)"),
    ("seizure", "Seizure mentioned"),
    ("worst headache", "Thunderclap / worst headache language"),
]
MODERATE_FLAGS: List[Tuple[str, str]] = [
    ("fever", "Fever present"), ("high fever", "High fever"), ("vomiting", "Vomiting"),
    ("unable to keep fluids", "Unable to keep fluids down"), ("dizziness", "Dizziness"),
    ("vertigo", "Vertigo / severe dizziness"), ("blood in urine", "Blood in urine"),
    ("blood in stool", "Blood in stool"), ("black stool", "Black stool"),
    ("burning sensation while urinating", "Dysuria (burning urination)"),
    ("painful urination", "Painful urination"), ("swelling", "Swelling reported"),
    ("rash with fever", "Rash associated with fever"), ("persistent vomiting", "Persistent vomiting"),
    ("dehydration", "Dehydration concern"), ("severe pain", "Severe pain"),
    ("uncontrolled pain", "Uncontrolled pain"), ("pregnancy", "Pregnancy mentioned – extra caution"),
    ("pregnant", "Pregnancy mentioned – extra caution"),
]
LOW_SIGNAL_SWELLING_CONTEXTS = ("after standing all day", "after standing for a long time", "after prolonged standing")

def assess_urgency(text: str) -> UrgencyResult:
    if not text or not text.strip():
        return UrgencyResult("low", 0, ["No concern text provided"], "Please describe the health concern.")
    lower=text.lower().strip(); score=0; reasons=[]
    for pattern,reason in HIGH_FLAGS:
        if pattern in lower:
            score+=10
            if reason not in reasons: reasons.append(reason)
    if "fever" in lower and "rash" in lower and ("severe headache" in lower or "worst headache" in lower or ("headache" in lower and "severe" in lower)):
        score+=10
        reason="Fever, rash, and severe headache combination detected"
        if reason not in reasons: reasons.append(reason)
    moderate_matches=[(p,r) for p,r in MODERATE_FLAGS if p in lower]
    if any(ctx in lower for ctx in LOW_SIGNAL_SWELLING_CONTEXTS):
        moderate_matches=[item for item in moderate_matches if item[0] != "swelling"]
    for _,reason in moderate_matches:
        score+=3
        if reason not in reasons: reasons.append(reason)
    if score>=10:
        level="high"; recommendation="High-priority signals matched by the prototype. If symptoms are currently severe or worsening, seek urgent medical care."
    elif score>=3:
        level="moderate"; recommendation="Moderate concern indicators matched. Monitor the situation and seek medical review if symptoms persist, worsen, or new concerning signs appear."
    else:
        level="low"; recommendation="No strong red-flag pattern matched the current description. Continue to monitor and seek care if the situation changes or does not improve."
    if not reasons: reasons.append("No specific red-flag keywords matched")
    return UrgencyResult(level, score, reasons, recommendation)
