"""Evaluate deterministic v2 review-workflow fixtures.
This is software evaluation, not clinical validation.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.response_engine import build_response

DATA_PATH = ROOT / "data" / "review_evaluation_set.json"


def main() -> int:
    cases = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    correct = 0
    failures = []
    for case in cases:
        response = build_response(case["input"], "synthetic", include_ebm=False)
        actual = response.safety_signal.status if response.safety_signal else "missing"
        if actual == case["expected_signal_status"]:
            correct += 1
        else:
            failures.append(
                f"{case['case_id']}: expected {case['expected_signal_status']}, got {actual}"
            )
    print(f"cases={len(cases)}")
    print(f"correct={correct}")
    print(
        f"accuracy={correct / len(cases):.2%}"
        if cases
        else "accuracy=0.00%"
    )
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
