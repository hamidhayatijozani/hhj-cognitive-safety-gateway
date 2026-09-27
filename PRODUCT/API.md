# Sbat API

## Health
GET /health

## Assess
POST /v1/assess

Request fields:
- decision_id
- agent_id
- action
- objective
- impact
- evidence[]
- policy
- metadata

The API returns an Assessment plus its Evidence Ledger record. Authentication, TLS, tenant isolation and production secret management belong at the deployment boundary and are not enabled by this minimal reference server.

## Example

```json
{
  "decision_id":"d-001",
  "agent_id":"agent-1",
  "action":"execute_transfer",
  "objective":"settle_invoice",
  "impact":"high",
  "evidence":[
    {"evidence_id":"invoice-1","source":"erp","content_hash":"sha256:...","reliability":0.95}
  ],
  "policy":{"policy_id":"finance","version":"3.2","min_evidence":1,"min_reliability":0.9}
}
```
