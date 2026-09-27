from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Mapping

class Verdict(str, Enum):
    APPROVE="APPROVE"; REJECT="REJECT"; REVIEW="REVIEW"; SANDBOX="SANDBOX"; DEFER="DEFER"

@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    source: str
    content_hash: str
    reliability: float = 1.0
    metadata: Mapping[str, Any] = field(default_factory=dict)
    def __post_init__(self):
        if not self.evidence_id or not self.source or not self.content_hash: raise ValueError("evidence_id, source, content_hash required")
        if not 0 <= self.reliability <= 1: raise ValueError("reliability must be between 0 and 1")

@dataclass(frozen=True)
class Proposal:
    decision_id: str
    agent_id: str
    action: str
    objective: str
    impact: str
    evidence: tuple[Evidence,...] = ()
    context: Mapping[str,Any] = field(default_factory=dict)

@dataclass(frozen=True)
class Policy:
    policy_id: str
    version: str
    min_evidence: int = 1
    min_reliability: float = .7
    blocked_impacts: tuple[str,...] = ()
    require_consensus: bool = False
    max_risk_score: float = .35

@dataclass(frozen=True)
class Assessment:
    decision_id: str
    verdict: Verdict
    risk_score: float
    evidence_coverage: float
    reasons: tuple[str,...]
    policy_id: str
    policy_version: str
    assessment_hash: str
    created_at: str
    def to_dict(self): return asdict(self)
