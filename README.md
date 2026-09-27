# Sbat

**Sbat** is an evidence-bound decision intelligence platform for evaluating, challenging, governing, and evidencing high-impact decisions made by AI agents and autonomous systems.

## What Sbat does

Sbat places an independent assessment boundary around an agent decision:

```
Agent / Workflow
      |
      v
Decision Proposal
      |
      v
Evidence Intake
      |
      v
Policy + Cognitive Risk Evaluation
      |
      +--> Red-Team Challenges
      +--> Multi-Agent Evaluation
      |
      v
Decision Assessment
      |
      +--> APPROVE
      +--> REJECT
      +--> REVIEW
      +--> SANDBOX
      +--> DEFER
      |
      v
Evidence Ledger
      |
      v
Assurance Report
```

Sbat assesses decisions. It does not execute the proposed action.

## Product capabilities

- deterministic policy-bound assessment
- cognitive risk signal with inspectable factors
- evidence coverage and reliability checks
- red-team scenario evaluation
- multi-agent agreement analysis
- chained, HMAC-protected evidence ledger
- replayable machine-readable assessments
- assurance reports
- Python service layer, CLI, and HTTP reference API
- automated tests and GitHub Actions CI

## Trust and claim boundary

Sbat does **not** claim to guarantee truth, eliminate hallucinations, certify legal admissibility, remove liability, perfectly predict risk, or guarantee business outcomes.

Cryptographic records provide integrity evidence within the defined trust boundary. Production legal effect depends on deployment, controls, jurisdiction, and applicable evidence rules.

## Repository structure

- `sbat/` product runtime and SDK surface
- `tests/` product and API tests
- `PRODUCT/` product, architecture, API, security and release documentation
- `pyproject.toml` Python package metadata

## Run

```bash
python -m unittest discover -s tests -p "test_*.py" -v
python -m sbat.cli --action "execute_transfer" --impact medium --evidence 2 --reliability .9
```

Reference API:

```bash
python -c "from sbat.api import serve; serve()"
```

Then call `GET /health` or `POST /v1/assess`.

## Product status

Sbat 1.0.0 is a functional reference product and commercial pilot foundation. Customer production deployment still requires deployment-specific security, persistence, authentication, tenant isolation, observability, performance validation, and contractual controls.

## License

TBD.
