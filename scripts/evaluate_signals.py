"""Evaluate the v1.2 medication-signal prototype on synthetic cases."""
from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from utils.clinical_data import extract_clinical_context
from utils.safety_signals import assess_safety_signal
DATA_PATH=ROOT/"data"/"signal_evaluation_set.json"
def main()->None:
    with DATA_PATH.open("r",encoding="utf-8") as handle: cases=json.load(handle)
    failures=[]; counts={}
    for case in cases:
        result=assess_safety_signal(extract_clinical_context(case["concern"],case.get("drug_name")))
        predicted=result.status; counts[predicted]=counts.get(predicted,0)+1
        if predicted!=case["expected_status"]: failures.append((case["id"],case["expected_status"],predicted))
    total=len(cases); correct=total-len(failures)
    print("\n=== MedFindr SignalGraph Evaluation ===")
    print(f"Cases evaluated    : {total}")
    print(f"Correct            : {correct}")
    print(f"Exact status match : {(correct/total*100) if total else 0:.1f}%")
    print("\nStatus counts")
    for key in sorted(counts): print(f"- {key}: {counts[key]}")
    if failures:
        print("\nFailures")
        for case_id,expected,predicted in failures: print(f"- {case_id}: expected={expected}, predicted={predicted}")
    else: print("\nAll synthetic signal cases passed.")
    print("\nNote: These synthetic cases test software behavior only. They are not pharmacovigilance validation, causality assessment, or clinical validation.")
if __name__=="__main__": main()
