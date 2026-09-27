from __future__ import annotations
import argparse,json
from .models import Evidence,Proposal,Policy
from .service import SbatService

def main():
    p=argparse.ArgumentParser(prog="sbat")
    p.add_argument("--action",required=True); p.add_argument("--impact",default="medium")
    p.add_argument("--evidence",type=int,default=1); p.add_argument("--reliability",type=float,default=.9)
    a=p.parse_args()
    ev=tuple(Evidence(f"e{i}","cli",f"hash-{i}",a.reliability) for i in range(a.evidence))
    proposal=Proposal("cli-decision","cli-agent",a.action,"cli-objective",a.impact,ev)
    assessment,_=SbatService(b"local-development-secret").assess(proposal,Policy("default","1.0"))
    print(json.dumps(assessment.to_dict(),indent=2,default=str))
if __name__=="__main__": main()
