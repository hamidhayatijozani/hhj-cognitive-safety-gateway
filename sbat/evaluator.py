from __future__ import annotations
import hashlib,json
from datetime import datetime,timezone
from .models import *
from .risk import CognitiveRiskEngine

class SbatEvaluator:
    def __init__(self,risk_engine=None): self.risk=CognitiveRiskEngine() if risk_engine is None else risk_engine
    def evaluate(self, proposal: Proposal, policy: Policy) -> Assessment:
        rr=self.risk.score(proposal,policy); n=len(proposal.evidence)
        coverage=1.0 if policy.min_evidence==0 else min(1.0,n/policy.min_evidence)
        reasons=list(rr.reasons)
        if proposal.impact in policy.blocked_impacts:
            verdict=Verdict.REJECT; reasons.append("impact_blocked_by_policy")
        elif n<policy.min_evidence:
            verdict=Verdict.REVIEW; reasons.append("minimum_evidence_not_met")
        elif any(e.reliability<policy.min_reliability for e in proposal.evidence):
            verdict=Verdict.REVIEW; reasons.append("evidence_reliability_below_policy_threshold")
        elif rr.score>policy.max_risk_score:
            verdict=Verdict.REVIEW; reasons.append("risk_score_above_policy_threshold")
        else: verdict=Verdict.APPROVE; reasons.append("policy_and_risk_requirements_satisfied")
        payload={"decision_id":proposal.decision_id,"verdict":verdict.value,"risk_score":rr.score,"coverage":coverage,"policy":policy.policy_id,"version":policy.version,"reasons":reasons}
        digest=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":")).encode()).hexdigest()
        return Assessment(proposal.decision_id,verdict,rr.score,coverage,tuple(reasons),policy.policy_id,policy.version,digest,datetime.now(timezone.utc).isoformat())
