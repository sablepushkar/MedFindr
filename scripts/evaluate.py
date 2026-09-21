"""
Evaluation script for MedFindr urgency engine.
Prints a clear agreement report against the labelled evaluation set.

Usage:
    python scripts/evaluate.py
"""

from __future__ import annotations

import json
from pathlib import Path

from utils.urgency import assess_urgency

ROOT = Path(__file__).parent.parent
EVAL_PATH = ROOT / "data" / "evaluation_set.json"


def main() -> None:
    if not EVAL_PATH.exists():
        print(f"Evaluation set not found at {EVAL_PATH}")
        return

    with open(EVAL_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    total = 0
    correct = 0
    results = []

    for item in data:
        concern = item.get("concern", "")
        expected = item.get("expected_urgency", "").lower().strip()
        result = assess_urgency(concern)
        predicted = result.level.lower()

        match = predicted == expected
        total += 1
        if match:
            correct += 1

        results.append({
            "id": item.get("id", ""),
            "concern": concern[:55] + ("..." if len(concern) > 55 else ""),
            "expected": expected,
            "predicted": predicted,
            "match": match,
        })

    accuracy = (correct / total * 100) if total else 0.0

    print("\n=== MedFindr Urgency Evaluation ===")
    print(f"Total cases  : {total}")
    print(f"Correct      : {correct}")
    print(f"Accuracy     : {accuracy:.1f}%\n")

    print(f"{'Status':<7} {'ID':<12} {'Expected':<10} {'Predicted':<10} Concern")
    print("-" * 85)

    for r in results:
        status = "PASS" if r["match"] else "FAIL"
        print(f"{status:<7} {r['id']:<12} {r['expected']:<10} {r['predicted']:<10} {r['concern']}")

    print("-" * 85)
    print("Note: This currently evaluates the rule-based urgency engine only.")
    print("EBM performance can be added once the trained model is actively used.\n")


if __name__ == "__main__":
    main()
