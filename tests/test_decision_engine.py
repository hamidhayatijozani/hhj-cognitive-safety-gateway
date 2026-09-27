import unittest
from hhj_decision_intelligence.evaluator import DecisionEvaluator
from hhj_decision_intelligence.models import DecisionProposal,EvidenceItem,EvidenceStatus,Policy,Verdict
class DecisionEngineTests(unittest.TestCase):
 def setUp(self): self.e=DecisionEvaluator(); self.p=Policy("enterprise-default","1.0",2,0.8)
 def ev(self,r=1.0,i="e"): return EvidenceItem(i,"system-of-record","abc123",r)
 def prop(self,ev=()): return DecisionProposal("dec-001","agent-001","create_invoice","settle_customer_order","medium",tuple(ev))
 def test_insufficient_evidence_requires_review(self):
  r=self.e.evaluate(self.prop((self.ev(),)),self.p); self.assertEqual(r.verdict,Verdict.REVIEW); self.assertEqual(r.evidence_status,EvidenceStatus.INSUFFICIENT)
 def test_low_reliability_requires_review(self):
  r=self.e.evaluate(self.prop((self.ev(.5,"e1"),self.ev(1,"e2"))),self.p); self.assertEqual(r.verdict,Verdict.REVIEW)
 def test_sufficient_evidence_is_approved(self):
  r=self.e.evaluate(self.prop((self.ev(1,"e1"),self.ev(1,"e2"))),self.p); self.assertEqual(r.verdict,Verdict.APPROVE); self.assertEqual(r.evidence_coverage,1.0)
 def test_blocked_impact_is_rejected(self):
  p=Policy("restricted","1.0",1,.7,("critical",)); q=DecisionProposal("critical","agent","delete_production_data","cleanup","critical",(self.ev(),)); self.assertEqual(self.e.evaluate(q,p).verdict,Verdict.REJECT)
if __name__=="__main__": unittest.main()
