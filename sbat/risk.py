from __future__ import annotations
from dataclasses import dataclass
from .models import Proposal, Policy

@dataclass(frozen=True)
class RiskResult:
    score: float
    factors: dict[str,float]
    reasons: tuple[str,...]

class CognitiveRiskEngine:
    """Deterministic, inspectable risk scoring. Score is an engineering signal, not truth probability."""
    def score(self, proposal: Proposal, policy: Policy) -> RiskResult:
        factors={}
        factors["impact"]= {"low":.05,"medium":.20,"high":.55,"critical":.85}.get(proposal.impact.lower(), .50)
        factors["evidence_gap"]= max(0.0,1.0-min(1.0,len(proposal.evidence)/max(policy.min_evidence,1)))
        factors["reliability_gap"]= 1.0-(sum(e.reliability for e in proposal.evidence)/len(proposal.evidence) if proposal.evidence else 0.0)
        factors["evidence_gap"]*=.35; factors["reliability_gap"]*=.35; factors["impact"]*=.30
        score=round(min(1.0,sum(factors.values())),6)
        reasons=[]
        if factors["evidence_gap"]>0: reasons.append("evidence_gap")
        if factors["reliability_gap"]>.15: reasons.append("reliability_gap")
        if factors["impact"]>.20: reasons.append("impact_risk")
        return RiskResult(score,factors,tuple(reasons))
