# Contributing

Small team, high bar. The rules below exist so that every artefact in this repo can be
defended in front of an auditor, a regulator and a hostile red-teamer.

## Workflow

1. Branch from `main`: `feat/<short-name>`, `fix/<short-name>`, or `adr/<short-name>`.
2. Open a PR. CI (lint, tests, secret scan) must be green.
3. One review before merge — Mohamed or MZ. No direct pushes to `main` once branch
   protection is on.

## Commit style

Plain imperative subject lines ("Add smoke eval task"), body explains *why* when it
isn't obvious. Reference ADRs where a commit implements one.

## The reproducibility checklist (applies to any eval or red-team change)

Before merging anything that produces a score or finding, confirm:

- [ ] Dependency versions pinned (lockfile updated if deps changed)
- [ ] Exact model ID, endpoint and generation parameters captured in the run config
- [ ] Seeds set where the stack supports them
- [ ] Inputs/outputs logged (Inspect `.eval` log or tool-native equivalent) and the
      log retained as the artefact of record
- [ ] Limitations and *what was not tested* stated in the accompanying doc
- [ ] Red-team findings mapped to OWASP LLM Top 10 categories

## Decisions

Consequential or hard-to-reverse choices get an ADR in `docs/adr/` (template:
`docs/adr/ADR-000-template.md`). PRs that change architecture without an ADR will be
bounced — kindly.

## UK English, precise, concrete

"We run N evaluations across M threat categories," not "world-class testing."
