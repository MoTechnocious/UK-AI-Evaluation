# /infra — CI, sandboxing and reproducibility plumbing

Bias: boring, open-source, near-zero spend. We are pre-seed; anything that adds a
monthly bill or a maintenance burden needs an ADR and Mohamed's sign-off.

## Current state

- **CI:** GitHub Actions (`.github/workflows/ci.yml`) — lint (ruff), tests (pytest),
  secret scan (gitleaks). Free tier.
- **Reference platform:** Linux. Local dev on anything; results that ship come from
  pinned, containerised runs.

## Next (in order, each gated on actually needing it)

1. Dockerfile for a pinned eval-runner image (the reproducibility substrate).
2. Lockfile discipline: `uv lock` checked in, CI installs from it.
3. Sandbox profile for red-team runs (container + no-network-by-default + allowlist).
4. Artefact retention: where `.eval` logs for published results live long-term.

## Rules of the room

- Model interactions are sandboxed; untrusted outputs are never executed or rendered
  outside the sandbox.
- Secrets only via CI secrets / `.env`. Least privilege on every token.
