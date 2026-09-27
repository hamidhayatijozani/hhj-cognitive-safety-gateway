# Sbat Architecture

```
Agent / Workflow
      |
      v
Decision Proposal API
      |
      +--> Evidence Intake
      +--> Policy Engine
      +--> Cognitive Risk Engine
      +--> Red-Team Engine
      +--> Multi-Agent Evaluation
      |
      v
Assessment
      |
      +--> Evidence Ledger
      +--> Assurance Report
      +--> Execution Adapter (optional, external)
```

Sbat assesses and evidences decisions. Execution remains outside the assessment core.

## Trust boundary

Inputs are untrusted. Policies are explicit versioned inputs. Assessment output is deterministic for identical proposal/policy/risk-engine versions except for timestamp metadata. Evidence records are chained and HMAC-protected.

## Deployment

The core is dependency-light Python and can run locally, in CI, behind an API service, or as a sidecar to an agent runtime.
