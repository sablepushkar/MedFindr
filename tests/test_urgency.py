"""Regression and contract tests for the MedFindr prototype."""
from __future__ import annotations
import json,unittest
from pathlib import Path
from unittest.mock import patch
from utils.response_engine import build_response
from utils.urgency import assess_urgency
ROOT=Path(__file__).resolve().parents[1]; EVAL_PATH=ROOT/"data"/"evaluation_set.json"
class UrgencyRegressionTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  with EVAL_PATH.open("r",encoding="utf-8") as f: cls.cases=json.load(f)
 def test_evaluation_set_matches_expected_labels(self):
  failures=[]
  for item in self.cases:
   result=assess_urgency(item["concern"]); expected=item["expected_urgency"].strip().lower()
   if result.level!=expected: failures.append(f'{item.get("id","<unknown>")}: expected {expected}, got {result.level}')
  self.assertEqual([],failures,"\n".join(failures))
 def test_empty_input_is_handled(self):
  result=assess_urgency(""); self.assertEqual(result.level,"low"); self.assertEqual(result.score,0); self.assertTrue(result.reasons)
 def test_high_flag_produces_high_urgency(self):
  result=assess_urgency("sudden chest pain"); self.assertEqual(result.level,"high"); self.assertGreaterEqual(result.score,10)
 def test_high_combination_rule(self): self.assertEqual(assess_urgency("high fever with rash and severe headache").level,"high")
 def test_contextual_swelling_case_remains_low(self): self.assertEqual(assess_urgency("ankle swelling after standing all day").level,"low")
 def test_reasons_are_not_duplicated(self):
  result=assess_urgency("chest pain and chest pain"); self.assertEqual(len(result.reasons),len(set(result.reasons)))
class ResponseEngineTests(unittest.TestCase):
 @patch("utils.response_engine.search_drug")
 def test_response_pipeline_is_structured(self,mock_search):
  mock_search.return_value={"status":"success","query":"example"}; response=build_response("sudden chest pain",drug_name="example")
  self.assertEqual(response.urgency.level,"high"); self.assertTrue(response.sections); self.assertEqual(response.drug_result["status"],"success"); self.assertEqual(response.to_dict()["urgency"]["level"],"high")
 def test_response_can_disable_ebm(self):
  response=build_response("headache",include_ebm=False); self.assertIsNone(response.ebm); self.assertEqual(response.urgency.level,"low")
if __name__=="__main__": unittest.main()
