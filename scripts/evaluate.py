"""Evaluate MedFindr's rule-based urgency engine against a labelled fixture.

Usage:
    python scripts/evaluate.py
    python scripts/evaluate.py --json-out evaluation-report.json

This is a software regression aid, not clinical validation.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.urgency import assess_urgency

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
    """Evaluate cases and reject malformed labels rather than hiding bad fixtures."""
    if not isinstance(cases, list):
        raise ValueError("Evaluation cases must be a list.")
    results = []
    seen_ids = set()
    for index, item in enumerate(cases):
        if not isinstance(item, dict):
            raise ValueError(f"Evaluation case {index} must be an object.")
        concern = item.get("concern")
        expected = item.get("expected_urgency")
        case_id = str(item.get("id", f"case_{index + 1}"))
        if not isinstance(concern, str) or not concern.strip():
            raise ValueError(f"Evaluation case {case_id} must have a non-empty concern.")
        if not isinstance(expected, str) or expected.strip().lower() not in LABELS:
            raise ValueError(f"Evaluation case {case_id} has an unknown expected_urgency label.")
        if case_id in seen_ids:
            raise ValueError(f"Duplicate evaluation case id: {case_id}")
        seen_ids.add(case_id)
        expected = expected.strip().lower()
        prediction = assess_urgency(concern).level.lower()
        results.append({
            "id": case_id,
            "concern": concern,
            "expected": expected,
            "predicted": prediction,
            "match": expected == prediction,
        })

    confusion = {expected: {predicted: 0 for predicted in LABELS} for expected in LABELS}
    for result in results:
        expected, predicted = result["expected"], result["predicted"]
        if predicted not in LABELS:
            raise ValueError(f"Rule engine returned unknown label: {predicted}")
        confusion[expected][predicted] += 1
    return results, confusion


def build_report(results: list[dict], confusion: dict) -> dict:
    total = len(results)
    correct = sum(bool(item["match"]) for item in results)
    per_class = {}
    for label in LABELS:
        true_positive = confusion[label][label]
        predicted_total = sum(confusion[expected][label] for expected in LABELS)
        support = sum(confusion[label].values())
        per_class[label] = {
            "precision": true_positive / predicted_total if predicted_total else 0.0,
            "recall": true_positive / support if support else 0.0,
            "support": support,
        }
    return {
        "project_version": "MedFindr X2",
        "evaluation_type": "rule-based regression fixture; not clinical validation",
        "total_cases": total,
        "correct_cases": correct,
        "accuracy_percent": round(correct / total * 100, 2) if total else 0.0,
        "confusion_matrix": confusion,
        "per_class": per_class,
        "cases": results,
    }


def print_report(report: dict) -> None:
    print("\n=== MedFindr Rule Evaluation ===")
    print(f"Total cases : {report['total_cases']}")
    print(f"Correct     : {report['correct_cases']}")
    print(f"Accuracy    : {report['accuracy_percent']:.1f}%")
    print("\nConfusion matrix (rows=expected, columns=predicted)")
    print(f"{'':<12}" + "".join(f"{label:>10}" for label in LABELS))
    print("-" * 42)
    for expected in LABELS:
        row = report["confusion_matrix"][expected]
        print(f"{expected:<12}" + "".join(f"{row[label]:>10}" for label in LABELS))
    print("\nPer-class metrics")
    print(f"{'Class':<12}{'Precision':>12}{'Recall':>12}{'Support':>12}")
    print("-" * 48)
    for label in LABELS:
        metrics = report["per_class"][label]
        print(f"{label:<12}{metrics['precision'] * 100:>11.1f}%{metrics['recall'] * 100:>11.1f}%{metrics['support']:>12}")
    failures = [item for item in report["cases"] if not item["match"]]
    if failures:
        print("\nCases to review")
        for item in failures:
            print(f"- {item['id']}: expected={item['expected']} predicted={item['predicted']} | {item['concern']}")
    else:
        print("\nAll labelled evaluation cases matched the current rules.")
    print("\nThis report evaluates a small rule-based fixture only. It does not establish clinical safety or effectiveness.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-out", type=Path, help="also write a machine-readable JSON report to this path")
    args = parser.parse_args()
    results, confusion = evaluate(load_cases())
    report = build_report(results, confusion)
    print_report(report)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"\nJSON report written to: {args.json_out}")


if __name__ == "__main__":
    main()
