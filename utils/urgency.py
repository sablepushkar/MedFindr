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
    ("cannot breathe", "Difficulty breathing / shortness of breath"),
    ("can't breathe", "Difficulty breathing / shortness of breath"),
    ("unable to breathe", "Difficulty breathing / shortness of breath"),
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
_NEGATION_PREFIXES = ("negative for", "without", "denies", "denied", "no", "not", "free of")


def _has_positive_phrase(text: str, phrase: str) -> bool:
    """Match a flag unless a simple, directly preceding negation is present.

    This deliberately handles only clear local negations; it is not clinical
    natural-language understanding and must not be treated as a rule-out tool.
    """
    start = 0
    while True:
        index = text.find(phrase, start)
        if index < 0:
            return False
        prefix = text[:index].rstrip()
        if not any(prefix.endswith(token) and (len(prefix) == len(token) or prefix[-len(token)-1].isspace()) for token in _NEGATION_PREFIXES):
            return True
        start = index + len(phrase)


def assess_urgency(text: str) -> UrgencyResult:
    if not text or not text.strip():
        return UrgencyResult("low", 0, ["No concern text provided"], "Please describe the health concern.")
    lower=text.lower().strip(); score=0; reasons=[]
    for pattern,reason in HIGH_FLAGS:
        if _has_positive_phrase(lower, pattern):
            score+=10
            if reason not in reasons: reasons.append(reason)
    if _has_positive_phrase(lower, "fever") and _has_positive_phrase(lower, "rash") and (_has_positive_phrase(lower, "severe headache") or _has_positive_phrase(lower, "worst headache") or (_has_positive_phrase(lower, "headache") and _has_positive_phrase(lower, "severe"))):
        score+=10
        reason="Fever, rash, and severe headache combination detected"
        if reason not in reasons: reasons.append(reason)
    matched_patterns = {pattern for pattern, _ in MODERATE_FLAGS if _has_positive_phrase(lower, pattern)}
    moderate_matches = []
    for pattern, reason in MODERATE_FLAGS:
        if pattern not in matched_patterns:
            continue
        # A specific phrase should not also score its contained generic phrase.
        # Example: "high fever" is one concept, not two independent findings.
        if any(pattern != specific and pattern in specific and specific in lower for specific in matched_patterns):
            continue
        moderate_matches.append((pattern, reason))
    if any(ctx in lower for ctx in LOW_SIGNAL_SWELLING_CONTEXTS):
        moderate_matches = [item for item in moderate_matches if item[0] != "swelling"]
    for _, reason in moderate_matches:
        score += 3
        if reason not in reasons:
            reasons.append(reason)
    if score>=10:
        level="high"; recommendation="High-priority signals matched by the prototype. If symptoms are currently severe or worsening, seek urgent medical care."
    elif score>=3:
        level="moderate"; recommendation="Moderate concern indicators matched. Monitor the situation and seek medical review if symptoms persist, worsen, or new concerning signs appear."
    else:
        level="low"; recommendation="No strong red-flag pattern matched the current description. Continue to monitor and seek care if the situation changes or does not improve."
    if not reasons: reasons.append("No specific red-flag keywords matched")
    return UrgencyResult(level, score, reasons, recommendation)
