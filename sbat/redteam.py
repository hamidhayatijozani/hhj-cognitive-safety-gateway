from __future__ import annotations
from dataclasses import dataclass
from .models import Proposal,Policy,Verdict
from .evaluator import SbatEvaluator

@dataclass(frozen=True)
class Scenario:
    name:str
    mutate:callable

@dataclass(frozen=True)
class ScenarioResult:
    name:str
    baseline:Verdict
    challenged:Verdict
    changed:bool
    reasons:tuple[str,...]

class RedTeamEngine:
    """Runs deterministic decision-challenge scenarios against the assessment boundary."""
    def __init__(self,evaluator=None): self.evaluator=evaluator or SbatEvaluator()
    def run(self,proposal,policy,scenarios):
        base=self.evaluator.evaluate(proposal,policy); out=[]
        for s in scenarios:
            challenged=s.mutate(proposal)
            a=self.evaluator.evaluate(challenged,policy)
            out.append(ScenarioResult(s.name,base.verdict,a.verdict,a.verdict!=base.verdict,a.reasons))
        return tuple(out)
    @staticmethod
    def default_scenarios():
        return (
            Scenario("remove_evidence",lambda p: Proposal(p.decision_id,p.agent_id,p.action,p.objective,p.impact,(),p.context)),
            Scenario("raise_impact",lambda p: Proposal(p.decision_id,p.agent_id,p.action,p.objective,"critical",p.evidence,p.context)),
        )
