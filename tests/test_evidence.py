import unittest
from hhj_decision_intelligence.evidence import EvidenceRecorder
from hhj_decision_intelligence.evaluator import DecisionEvaluator
from hhj_decision_intelligence.models import DecisionProposal,EvidenceItem,Policy
class EvidenceTests(unittest.TestCase):
 def test_record_is_stable(self):
  q=DecisionProposal("d","a","approve_refund","resolve","medium",(EvidenceItem("e","crm","hash",1.0),)); a=DecisionEvaluator().evaluate(q,Policy("p","1",1)); r=EvidenceRecorder(b"test-secret"); x=r.record(a); y=r.record(a); self.assertEqual(x["record_hash"],y["record_hash"]); self.assertEqual(x["hmac_sha256"],y["hmac_sha256"])
if __name__=="__main__": unittest.main()
