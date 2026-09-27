from __future__ import annotations
import json
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from .models import Evidence,Proposal,Policy
from .service import SbatService

def create_handler(service):
    class Handler(BaseHTTPRequestHandler):
        def send_json(self,status,payload):
            body=json.dumps(payload,default=str).encode()
            self.send_response(status); self.send_header("Content-Type","application/json"); self.send_header("Content-Length",str(len(body))); self.end_headers(); self.wfile.write(body)
        def do_GET(self):
            if self.path=="/health": return self.send_json(200,{"status":"ok","product":"Sbat","version":"1.0.0"})
            return self.send_json(404,{"error":"not_found"})
        def do_POST(self):
            if self.path!="/v1/assess": return self.send_json(404,{"error":"not_found"})
            try:
                n=int(self.headers.get("Content-Length","0")); data=json.loads(self.rfile.read(n))
                evidence=tuple(Evidence(**e) for e in data.get("evidence",[]))
                p=Proposal(data["decision_id"],data["agent_id"],data["action"],data.get("objective",""),data.get("impact","medium"),evidence,data.get("context",{}))
                q=data.get("policy",{}); policy=Policy(q.get("policy_id","default"),q.get("version","1.0"),q.get("min_evidence",1),q.get("min_reliability",.7),tuple(q.get("blocked_impacts",())),q.get("require_consensus",False),q.get("max_risk_score",.35))
                a,record=service.assess(p,policy,data.get("metadata"))
                return self.send_json(200,{"assessment":a.to_dict(),"record":record})
            except (KeyError,ValueError,TypeError,json.JSONDecodeError) as e: return self.send_json(400,{"error":"invalid_request","detail":str(e)})
    Handler.log_message=lambda *args: None
    return Handler

def serve(host="127.0.0.1",port=8080,secret=b"development-secret"):
    service=SbatService(secret); ThreadingHTTPServer((host,port),create_handler(service)).serve_forever()
