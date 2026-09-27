import unittest
from sbat.models import Evidence,Proposal,Policy,Verdict
from sbat.evaluator import SbatEvaluator
from sbat.ledger import EvidenceLedger
from sbat.redteam import RedTeamEngine
from sbat.consensus import MultiAgentEvaluator

class SbatProductTests(unittest.TestCase):
    def setUp(self):
        self.policy=Policy("p","1.0",min_evidence=2,min_reliability=.8,max_risk_score=.55)
        self.ev=(Evidence("e1","db","h1",.95),Evidence("e2","api","h2",.9))
        self.p=Proposal("d1","agent-a","execute","objective","low",self.ev)
    def test_approve_and_ledger(self):
        a=SbatEvaluator().evaluate(self.p,self.policy); self.assertEqual(a.verdict,Verdict.APPROVE)
        l=EvidenceLedger(b"secret"); l.append(a); self.assertTrue(l.verify())
    def test_review_missing_evidence(self):
        p=Proposal("d2","agent-a","execute","objective","low",self.ev[:1])
        self.assertEqual(SbatEvaluator().evaluate(p,self.policy).verdict,Verdict.REVIEW)
    def test_reject_blocked_impact(self):
        p=Proposal("d3","agent-a","execute","objective","critical",self.ev)
        policy=Policy("p","1.0",2,.8,("critical",),max_risk_score=.9)
        self.assertEqual(SbatEvaluator().evaluate(p,policy).verdict,Verdict.REJECT)
    def test_red_team_changes_evidence(self):
        out=RedTeamEngine().run(self.p,self.policy,RedTeamEngine.default_scenarios())
        self.assertTrue(any(x.changed for x in out))
    def test_consensus(self):
        p2=Proposal("d1","agent-b","execute","objective","low",self.ev)
        c=MultiAgentEvaluator().evaluate((self.p,p2),self.policy)
        self.assertEqual(c.verdict,Verdict.APPROVE); self.assertEqual(c.agreement,1.0)
if __name__=="__main__": unittest.main()
