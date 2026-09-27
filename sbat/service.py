from __future__ import annotations
from .evaluator import SbatEvaluator
from .ledger import EvidenceLedger
from .report import AssuranceReport

class SbatService:
    def __init__(self,secret:bytes):
        self.evaluator=SbatEvaluator(); self.ledger=EvidenceLedger(secret); self.reporter=AssuranceReport()
    def assess(self,proposal,policy,metadata=None):
        assessment=self.evaluator.evaluate(proposal,policy)
        record=self.ledger.append(assessment,metadata)
        return assessment,record
    def assurance_report(self,assessment,redteam=None,consensus=None):
        return self.reporter.build(assessment,self.ledger.verify(),redteam,consensus)
