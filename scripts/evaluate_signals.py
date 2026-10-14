"""Reproducible evaluation for MedFindr's synthetic medication-signal fixtures."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.clinical_data import extract_clinical_context
from utils.safety_signals import assess_safety_signal

DATA_PATH = ROOT / "data" / "signal_evaluation_set.json"
ALLOWED_STATUSES = {
    "flagged",
    "context_incomplete",
    "not_assessed",
    "insufficient_context",
}


def validate_cases(cases: Any) -> None:
    """Reject malformed evaluation fixtures before calculating metrics."""
    if not isinstance(cases, list) or not cases:
        raise ValueError("Signal evaluation fixture must be a non-empty JSON list.")

    seen_ids: set[str] = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            raise ValueError(f"Case {index + 1} must be a JSON object.")
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id.strip():
            raise ValueError(f"Case {index + 1} must have a non-empty string id.")
        if case_id in seen_ids:
            raise ValueError(f"Duplicate signal evaluation case id: {case_id}")
        seen_ids.add(case_id)

        concern = case.get("concern")
        if not isinstance(concern, str) or not concern.strip():
            raise ValueError(f"Case {case_id} must have a non-empty concern.")
        drug_name = case.get("drug_name", "")
        if not isinstance(drug_name, str):
            raise ValueError(f"Case {case_id} drug_name must be a string.")
        expected = case.get("expected_status")
        if not isinstance(expected, str) or expected not in ALLOWED_STATUSES:
            raise ValueError(
                f"Case {case_id} has unknown expected_status: {expected!r}"
            )


def load_cases(path: Path = DATA_PATH) -> tuple[list[dict[str, Any]], bytes]:
    raw = path.read_bytes()
    try:
        cases = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Could not parse signal evaluation fixture: {exc}") from exc
    validate_cases(cases)
    return cases, raw


def evaluate_cases(cases: list[dict[str, Any]]) -> dict[str, Any]:
    validate_cases(cases)
    failures: list[dict[str, str]] = []
    counts: dict[str, int] = {}
    for case in cases:
        context = extract_clinical_context(
            case["concern"], case.get("drug_name") or None
        )
        predicted = assess_safety_signal(context).status
        counts[predicted] = counts.get(predicted, 0) + 1
        if predicted != case["expected_status"]:
            failures.append({
                "case_id": case["id"],
                "expected_status": case["expected_status"],
                "predicted_status": predicted,
            })

    total = len(cases)
    matched = total - len(failures)
    return {
        "project": "MedFindr",
        "report_schema_version": 1,
        "evaluation_scope": (
            "Synthetic software-behavior regression only; not clinical, "
            "pharmacovigilance, or real-world validation."
        ),
        "case_count": total,
        "matched_count": matched,
        "agreement_percent": round((matched / total) * 100, 2) if total else 0.0,
        "status_counts": dict(sorted(counts.items())),
        "mismatches": failures,
    }


def build_report(
    cases: list[dict[str, Any]],
    raw_fixture: bytes,
    fixture_name: str = DATA_PATH.name,
) -> dict[str, Any]:
    report = evaluate_cases(cases)
    report["fixture"] = {
        "path": fixture_name,
        "sha256": hashlib.sha256(raw_fixture).hexdigest(),
    }
    report["source_revision"] = os.environ.get("GITHUB_SHA", "local-unpinned")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json-out",
        type=Path,
        help="write a machine-readable report to this path",
    )
    args = parser.parse_args()

    try:
        cases, raw_fixture = load_cases()
        report = build_report(cases, raw_fixture)
    except (OSError, ValueError) as exc:
        print(f"Evaluation could not run: {exc}", file=sys.stderr)
        return 2

    print("=== MedFindr Synthetic Signal Evaluation ===")
    print(f"Cases evaluated    : {report['case_count']}")
    print(f"Exact status match : {report['agreement_percent']:.2f}%")
    print(f"Fixture SHA-256    : {report['fixture']['sha256']}")
    print(f"Source revision    : {report['source_revision']}")
    for mismatch in report["mismatches"]:
        print(
            f"- {mismatch['case_id']}: expected={mismatch['expected_status']}, "
            f"predicted={mismatch['predicted_status']}"
        )
    print(
        "Scope: synthetic software-behavior checks only; "
        "not clinical or pharmacovigilance validation."
    )

    if args.json_out:
        try:
            args.json_out.parent.mkdir(parents=True, exist_ok=True)
            args.json_out.write_text(
                json.dumps(report, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
        except OSError as exc:
            print(f"Could not write JSON report: {exc}", file=sys.stderr)
            return 2
        print(f"JSON report        : {args.json_out}")

    return 1 if report["mismatches"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
