# Sbat

Sbat is an independent decision-intelligence platform for evaluating, governing, and evidencing high-impact decisions made by AI agents and autonomous systems.

## Product boundary

Sbat is a decision-assurance system. It evaluates decision proposals against explicit policies, evidence requirements, risk constraints, and provenance rules before producing a structured assessment.

It does **not** claim to guarantee truth, eliminate hallucinations, certify legal admissibility, remove liability, or predict business outcomes.

## Core flow

```
Decision Proposal
      |
      v
Evidence Intake
      |
      v
Risk & Policy Evaluation
      |
      v
Decision Assessment
      |
      +----> APPROVE
      +----> REJECT
      +----> REVIEW
      +----> SANDBOX
      +----> DEFER
      |
      v
Evidence Record / Replay
```

## Initial capabilities

- deterministic decision assessment
- evidence coverage and provenance tracking
- explicit risk constraints
- tamper-evident evidence records
- replayable assessment records
- policy version binding
- machine-readable assurance results
- clean separation between assessment and execution

## Status

Foundation release: Sbat is being built as a standalone product, independent of the HamidCognition Action Gate product.

## License

TBD.
