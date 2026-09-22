"""Evaluate MedFindr's rule-based urgency engine.

Usage:
    python scripts/evaluate.py
"""

from __future__ import annotations

import json
from pathlib import Path

from utils.urgency import assess_urgency

ROOT = Path(__file__).parent.parent
EVAL_PATH = ROOT / "data" / "evaluation_set.json"
LABELS = ("low", "moderate", "high")


def load_cases() -> list[dict]:
    if not EVAL_PATH.exists():
        raise FileNotFoundError(f"Evaluation set not found at {EVAL_PATH}")
    with EVAL_PATH.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError("Evaluation set must contain a JSON list.")
    return data


def evaluate(cases: list[dict]) -> tuple[list[dict], dict]:
    results = []
    for item in cases:
        concern = str(item.get("concern", ""))
        expected = str(item.get("expected_urgency", "")).strip().lower()
        predicted = assess_urgency(concern).level.lower()
        results.append({
            "id": item.get("id", ""),
            "concern": concern,
            "expected": expected,
            "predicted": predicted,
            "match": expected == predicted,
        })

    confusion = {
        expected: {predicted: 0 for predicted in LABELS}
        for expected in LABELS
    }
    for result in results:
        expected = result["expected"]
        predicted = result["predicted"]
        if expected in confusion and predicted in LABELS:
            confusion[expected][predicted] += 1

    return results, confusion


def print_report(results: list[dict], confusion: dict) -> None:
    total = len(results)
    correct = sum(item["match"] for item in results)
    accuracy = (correct / total * 100) if total else 0.0

    print("\n=== MedFindr Urgency Evaluation ===")
    print(f"Total cases : {total}")
    print(f"Correct     : {correct}")
    print(f"Accuracy    : {accuracy:.1f}%")

    print("\nConfusion matrix (rows=expected, columns=predicted)")
    print(f"{'':<12}" + "".join(f"{label:>10}" for label in LABELS))
    print("-" * 42)
    for expected in LABELS:
        row = confusion[expected]
        print(f"{expected:<12}" + "".join(f"{row[label]:>10}" for label in LABELS))

    print("\nPer-class metrics")
    print(f"{'Class':<12}{'Precision':>12}{'Recall':>12}{'Support':>12}")
    print("-" * 48)
    for label in LABELS:
        true_positive = confusion[label][label]
        predicted_total = sum(confusion[expected][label] for expected in LABELS)
        support = sum(confusion[label].values())
        precision = true_positive / predicted_total if predicted_total else 0.0
        recall = true_positive / support if support else 0.0
        print(
            f"{label:<12}"
            f"{precision * 100:>11.1f}%"
            f"{recall * 100:>11.1f}%"
            f"{support:>12}"
        )

    failures = [item for item in results if not item["match"]]
    if failures:
        print("\nFailures")
        for item in failures:
            print(
                f"- {item['id']}: expected={item['expected']} "
                f"predicted={item['predicted']} | {item['concern']}"
            )
    else:
        print("\nAll labelled evaluation cases passed.")

    print(
        "\nNote: This evaluates the rule-based urgency engine only. "
        "It is not clinical validation and does not establish medical safety or effectiveness."
    )


def main() -> None:
    cases = load_cases()
    results, confusion = evaluate(cases)
    print_report(results, confusion)


if __name__ == "__main__":
    main()
