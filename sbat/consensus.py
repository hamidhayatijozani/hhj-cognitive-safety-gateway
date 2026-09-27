from __future__ import annotations
from dataclasses import dataclass
from .models import Proposal,Policy,Verdict
from .evaluator import SbatEvaluator

@dataclass(frozen=True)
class AgentAssessment:
    agent_id:str
    verdict:Verdict
    risk_score:float
    assessment_hash:str

@dataclass(frozen=True)
class ConsensusResult:
    verdict:Verdict
    agreement:float
    assessments:tuple[AgentAssessment,...]
    reason:str

class MultiAgentEvaluator:
    def __init__(self,evaluator=None): self.evaluator=evaluator or SbatEvaluator()
    def evaluate(self,proposals,policy):
        aa=tuple(AgentAssessment(p.agent_id,(a:=self.evaluator.evaluate(p,policy)).verdict,a.risk_score,a.assessment_hash) for p in proposals)
        if not aa: return ConsensusResult(Verdict.DEFER,0.0,(), "no_agent_assessments")
        counts={}
        for a in aa: counts[a.verdict]=counts.get(a.verdict,0)+1
        verdict,count=max(counts.items(),key=lambda x:(x[1],x[0].value))
        agreement=count/len(aa)
        if agreement<.67: verdict=Verdict.REVIEW
        return ConsensusResult(verdict,agreement,aa,"majority_consensus" if agreement>=.67 else "insufficient_agent_agreement")
