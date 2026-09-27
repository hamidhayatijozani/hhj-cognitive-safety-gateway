from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping

class Verdict(str, Enum):
    APPROVE="APPROVE"; REJECT="REJECT"; REVIEW="REVIEW"; SANDBOX="SANDBOX"; DEFER="DEFER"
class EvidenceStatus(str, Enum):
    SUFFICIENT="SUFFICIENT"; INSUFFICIENT="INSUFFICIENT"; CONFLICTING="CONFLICTING"
@dataclass(frozen=True)
class EvidenceItem:
    evidence_id:str; source:str; content_hash:str; reliability:float=1.0; metadata:Mapping[str,Any]=field(default_factory=dict)
    def __post_init__(self):
        if not self.evidence_id or not self.source or not self.content_hash: raise ValueError("evidence_id, source, and content_hash are required")
        if not 0.0 <= self.reliability <= 1.0: raise ValueError("reliability must be between 0 and 1")
@dataclass(frozen=True)
class DecisionProposal:
    decision_id:str; actor_id:str; action:str; objective:str; impact_level:str; evidence:tuple[EvidenceItem,...]=()
    def __post_init__(self):
        if not self.decision_id or not self.actor_id or not self.action: raise ValueError("decision_id, actor_id, and action are required")
@dataclass(frozen=True)
class Policy:
    policy_id:str; version:str; minimum_evidence:int=1; minimum_reliability:float=0.7; blocked_impacts:tuple[str,...]=()
    def __post_init__(self):
        if self.minimum_evidence < 0: raise ValueError("minimum_evidence cannot be negative")
        if not 0.0 <= self.minimum_reliability <= 1.0: raise ValueError("minimum_reliability must be between 0 and 1")
@dataclass(frozen=True)
class Assessment:
    decision_id:str; verdict:Verdict; evidence_status:EvidenceStatus; evidence_coverage:float
    policy_id:str; policy_version:str; reasons:tuple[str,...]; assessment_hash:str; created_at:str
