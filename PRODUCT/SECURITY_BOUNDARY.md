# Sbat Security Boundary

Sbat protects assessment integrity and evidence provenance within its defined trust boundary.

It does not automatically make an upstream model trustworthy. Callers must authenticate and authorize access to Sbat in production.

Recommended production controls:
- TLS termination
- authentication and RBAC
- tenant isolation
- secret management outside source control
- immutable/append-only evidence storage
- key rotation
- audit retention
- replay verification
- rate limiting
- dependency and supply-chain scanning
