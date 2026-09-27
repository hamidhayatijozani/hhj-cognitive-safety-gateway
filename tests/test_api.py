import json,unittest
from sbat.api import create_handler
from sbat.service import SbatService
from http.client import HTTPConnection
from threading import Thread
from http.server import ThreadingHTTPServer

class ApiTests(unittest.TestCase):
    def test_health_and_assess(self):
        server=ThreadingHTTPServer(("127.0.0.1",0),create_handler(SbatService(b"secret")))
        Thread(target=server.serve_forever,daemon=True).start()
        c=HTTPConnection("127.0.0.1",server.server_port)
        c.request("GET","/health"); r=c.getresponse(); self.assertEqual(r.status,200); r.read()
        body=json.dumps({"decision_id":"d","agent_id":"a","action":"test","objective":"x","impact":"low","evidence":[{"evidence_id":"e","source":"test","content_hash":"h","reliability":.95}]}).encode()
        c.request("POST","/v1/assess",body,{"Content-Type":"application/json"}); r=c.getresponse(); data=json.loads(r.read()); self.assertEqual(r.status,200); self.assertEqual(data["assessment"]["verdict"],"APPROVE")
        server.shutdown()
