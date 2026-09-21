"""
Simple evaluation script for MedFindr urgency engine.
Version: V09 Evolve

Runs the current rule-based urgency assessment against the evaluation set
and prints a clear agreement report.

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
        expected = item.get("expected_urgency", "").lower()
        result = assess_urgency(concern)
        predicted = result.level.lower()

        match = predicted == expected
        total += 1
        if match:
            correct += 1

        results.append({
            "id": item.get("id"),
            "concern": concern[:60] + ("..." if len(concern) > 60 else ""),
            "expected": expected,
            "predicted": predicted,
            "match": match,
        })

    accuracy = (correct / total * 100) if total else 0.0

    print("\n=== MedFindr Urgency Evaluation ===")
    print(f"Total cases     : {total}")
    print(f"Correct         : {correct}")
    print(f"Accuracy        : {accuracy:.1f}%")
    print("\nDetailed results:")
    print("-" * 80)

    for r in results:
        status = "✓" if r["match"] else "✗"
        print(f"{status} [{r['id']}] expected={r['expected']:<8} predicted={r['predicted']:<8} | {r['concern']}")

    print("-" * 80)
    print("Note: This evaluates only the rule-based urgency engine.")
    print("EBM evaluation can be added once a trained model is in active use.\n")


if __name__ == "__main__":
    main()
