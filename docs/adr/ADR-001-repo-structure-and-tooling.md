# ADR-001: Monorepo structure and tooling standard

## Status

accepted (2026-06-10)

## Context

UK AI Evaluation is pre-seed, two core engineers (Mohamed, MZ), near-zero budget. The
product is independent, audit-grade, **reproducible** assurance for high-stakes AI —
health/clinical-diagnostics first. Engineering choices must minimise maintenance burden,
maximise auditability, and align with the tooling regulators and frontier-lab safety
teams already trust.

## Decision

- **Single GitHub monorepo** (`MoTechnocious/UK-AI-Evaluation`) with top-level
  `/evals`, `/redteam`, `/reports`, `/infra`, `/docs`.
- **Evaluation harness: Inspect (UK AISI).** Every evaluation is an Inspect
  task/solver/scorer unless an ADR documents why not. The `.eval` log is the artefact
  of record.
- **Red-team tooling: garak, PyRIT, promptfoo.** Findings map to the OWASP LLM Top 10.
- **Languages: Python** (evals/orchestration) **and Rust** (where determinism,
  performance or hardened binaries matter). **Linux** is the reference platform.
- **CI: GitHub Actions free tier** — ruff lint, pytest, gitleaks secret scan on every
  push/PR. No paid CI, no self-hosted runners, until a pilot demands them.
- **Dependency pinning** via lockfile (`uv lock` on Linux); version ranges in
  `pyproject.toml` are specs, the lockfile is the reproducibility pin.

## Consequences

- Easier: one place for the whole methodology; cross-references between evals, findings
  and reports are repo-relative; one CI; agents and grant drafts cite a single URL.
- Harder: repo will mix Python and Rust toolchains; if the Evidence Base grows large
  datasets we will need LFS or external artefact storage (decide then, not now).
- Bet: Inspect remains the UK-AISI-aligned standard. Its trajectory and adoption make
  this a safe bet; the task abstraction is portable if not.

## Alternatives considered

- **Polyrepo (one repo per tool/area):** more isolation, but multiplies CI, access
  control and cross-referencing overhead a two-person team can't carry.
- **Bespoke eval harness:** maximum control, but we'd be selling assurance built on
  unaudited home-grown infrastructure — the opposite of the brand. Rejected.
- **promptfoo as the primary harness:** good for regression suites (we still use it in
  `/redteam`), but Inspect's logging, solver/scorer model and AISI provenance fit the
  audit-grade positioning better.
