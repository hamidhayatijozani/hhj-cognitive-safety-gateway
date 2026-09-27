from __future__ import annotations
import json
from dataclasses import asdict
class AssuranceReport:
    def build(self,assessment,ledger_ok=True,redteam=None,consensus=None):
        return {
          "product":"Sbat","report_version":"1.0",
          "assessment":asdict(assessment),
          "evidence_integrity":{"ledger_verified":ledger_ok},
          "red_team":{"scenarios":len(redteam or ()), "changed_verdicts":sum(x.changed for x in (redteam or ()))},
          "multi_agent":{"agreement":getattr(consensus,"agreement",None),"verdict":getattr(getattr(consensus,"verdict",None),"value",None)},
          "boundary":"This report describes Sbat assessment evidence; it is not a guarantee of truth, safety, legal admissibility, or business outcome."
        }
    def json(self,**kwargs): return json.dumps(self.build(**kwargs),sort_keys=True,indent=2,default=str)
