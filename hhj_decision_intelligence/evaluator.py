from __future__ import annotations
import hashlib,json
from datetime import datetime,timezone
from .models import Assessment,DecisionProposal,EvidenceStatus,Policy,Verdict
class DecisionEvaluator:
    """Deterministic assessment engine. It assesses; it never executes."""
    def evaluate(self,proposal:DecisionProposal,policy:Policy)->Assessment:
        n=len(proposal.evidence); coverage=1.0 if policy.minimum_evidence==0 else min(1.0,n/policy.minimum_evidence)
        reasons=[]
        if proposal.impact_level in policy.blocked_impacts:
            verdict=Verdict.REJECT; status=EvidenceStatus.SUFFICIENT if n else EvidenceStatus.INSUFFICIENT; reasons.append("impact_level_blocked_by_policy")
        elif n < policy.minimum_evidence:
            verdict=Verdict.REVIEW; status=EvidenceStatus.INSUFFICIENT; reasons.append("minimum_evidence_not_met")
        elif any(e.reliability < policy.minimum_reliability for e in proposal.evidence):
            verdict=Verdict.REVIEW; status=EvidenceStatus.INSUFFICIENT; reasons.append("evidence_reliability_below_policy_threshold")
        else:
            verdict=Verdict.APPROVE; status=EvidenceStatus.SUFFICIENT; reasons.append("policy_requirements_satisfied")
        payload={"decision_id":proposal.decision_id,"verdict":verdict.value,"evidence_status":status.value,"evidence_coverage":coverage,"policy_id":policy.policy_id,"policy_version":policy.version,"reasons":reasons}
        digest=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":")).encode()).hexdigest()
        return Assessment(proposal.decision_id,verdict,status,coverage,policy.policy_id,policy.version,tuple(reasons),digest,datetime.now(timezone.utc).isoformat())
