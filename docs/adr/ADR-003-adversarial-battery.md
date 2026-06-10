# ADR-003: Adversarial test battery — format, placement and scoring

## Status

accepted (2026-06-10)

## Context

We need a reusable adversarial test battery (AAT-2) we can run against any client AI
system as part of an AI Assurance Report. It must be: reproducible (our brand), legible
to security buyers (OWASP-mapped), health-first (our vertical), and runnable through the
standard harness. Three design questions: what format the cases live in, where they sit
in the monorepo, and how PASS/FAIL is decided.

## Decision

- **Canonical format: a versioned JSONL dataset** at
  `evals/datasets/adversarial-battery-v1/battery.jsonl`. One self-contained record per
  case with `id`, `category`, `owasp`, `technique`, `severity`, `input`, `pass_criteria`,
  `expected_behavior`, `fail_signals`. JSONL is diff-friendly, trivially loadable by
  Inspect, and tool-agnostic (garak/PyRIT/promptfoo can also consume it).
- **Placement under `/evals`, consumed by an Inspect task**, with a pointer from
  `/redteam`. Per ADR-001 every evaluation is an Inspect task and the `.eval` log is the
  artefact of record; routing the battery through Inspect gives us that logging and
  reproducibility for free. The battery is red-team *content* surfaced through the eval
  harness — hence the cross-reference rather than a second home.
- **Model-graded scoring against each case's own `pass_criteria`.** PASS = the system
  resisted (refused, ignored the injection, stayed in scope, gave safe advice). The
  grader's reasoning is logged; the parse is conservative (only an explicit `GRADE: PASS`
  passes). A separate `grader_model` parameter keeps the judge independent of the target.
- **Versioned as a directory.** v2 is a new directory; v1 is never silently mutated, so
  historical report scores stay reproducible.
- **No operational harmful detail, no real data.** Harmful-content cases use bracketed
  placeholders and test refusal; all identifiers are fabricated. Keeps the battery safe
  to store, share and upstream.

## Consequences

- Easier: one command runs the battery and produces an auditable `.eval` log; cases are
  cited by stable ID in findings and reports; CI (`tests/test_adversarial_battery.py`)
  enforces schema, per-category counts and ID uniqueness.
- Harder: model-graded PASS/FAIL is subjective and costs grader tokens; mitigated by
  logged reasoning, a conservative parse, and spot-checking. Agentic (tool-abuse) cases
  against a chat-only target grade stated intent, a weaker signal than an observed call.
- Bet: a fixed battery is a floor, not a guarantee. Reports must state this explicitly —
  an unstated limitation is an overclaim.

## Alternatives considered

- **Substring/keyword scorer on `fail_signals`:** cheap and deterministic, but brittle
  and easily evaded by paraphrase; kept as a human-review aid, not the scorer of record.
- **Human-only grading:** highest fidelity, doesn't scale to every run; we grade by model
  and human-audit a sample instead.
- **promptfoo redteam as the primary harness:** strong for regression suites (still used
  in `/redteam`), but Inspect's logging and AISI provenance fit the audit-grade
  positioning better, consistent with ADR-001.
- **Bury the cases inside the task `.py`:** faster to write, but couples data to code,
  blocks reuse by other tools, and makes versioning/diffing the battery painful.
