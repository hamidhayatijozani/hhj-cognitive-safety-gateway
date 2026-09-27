from __future__ import annotations
import hashlib,hmac,json
from dataclasses import asdict
class EvidenceLedger:
    def __init__(self,secret:bytes): 
        if not secret: raise ValueError("secret required")
        self.secret=secret; self.records=[]
    def append(self,assessment,metadata=None):
        body={"sequence":len(self.records)+1,"assessment":asdict(assessment),"metadata":metadata or {},"previous_hash":self.records[-1]["record_hash"] if self.records else None}
        raw=json.dumps(body,sort_keys=True,separators=(",",":"),default=str).encode()
        rec={**body,"record_hash":hashlib.sha256(raw).hexdigest(),"hmac_sha256":hmac.new(self.secret,raw,hashlib.sha256).hexdigest()}
        self.records.append(rec); return rec
    def verify(self):
        prev=None
        for i,r in enumerate(self.records,1):
            if r["sequence"]!=i or r["previous_hash"]!=prev: return False
            body={k:r[k] for k in ("sequence","assessment","metadata","previous_hash")}
            raw=json.dumps(body,sort_keys=True,separators=(",",":"),default=str).encode()
            if hashlib.sha256(raw).hexdigest()!=r["record_hash"]: return False
            if not hmac.compare_digest(hmac.new(self.secret,raw,hashlib.sha256).hexdigest(),r["hmac_sha256"]): return False
            prev=r["record_hash"]
        return True
