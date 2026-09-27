from __future__ import annotations
import hashlib,hmac,json
from dataclasses import asdict
from typing import Any
from .models import Assessment
class EvidenceRecorder:
    """Creates tamper-evident records; HMAC is integrity evidence, not legal admissibility."""
    def __init__(self,secret:bytes):
        if not secret: raise ValueError("secret is required")
        self._secret=secret
    def record(self,assessment:Assessment,previous_hash:str|None=None)->dict[str,Any]:
        body={"assessment":asdict(assessment),"previous_hash":previous_hash}
        canonical=json.dumps(body,sort_keys=True,separators=(",",":"),default=str).encode()
        return {**body,"record_hash":hashlib.sha256(canonical).hexdigest(),"hmac_sha256":hmac.new(self._secret,canonical,hashlib.sha256).hexdigest()}
