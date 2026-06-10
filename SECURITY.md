# Security Policy

We are an assurance company; our own security posture has to survive the scrutiny we
apply to others. We are working toward Cyber Essentials — we do not yet hold it, and we
claim no certification.

## Reporting a vulnerability

Email **inquiries@ukaiassurance.com** with subject `SECURITY`. Please include
reproduction steps and impact. We will acknowledge within 5 working days. Please do not
open a public issue for security reports.

## Rules we hold ourselves to in this repo

- **No secrets in git.** API keys and credentials live in `.env` (gitignored) or GitHub
  Actions secrets. CI runs a gitleaks scan on every push and PR; a hit is a blocker.
- **Least privilege.** Tokens are scoped to the minimum needed; personal access tokens
  are fine-grained and expiring.
- **Untrusted model I/O is untrusted input.** Eval and red-team runs execute in
  sandboxed/containerised environments (see `/infra`); model outputs are never executed
  or rendered unsandboxed.
- **All pilot data is sensitive.** Clinical-adjacent data raises the bar: no real
  patient data enters this repository under any circumstances. Datasets are synthetic,
  public, or licensed — with provenance recorded.
- **Assume any artefact may end up in front of a regulator or auditor.**
