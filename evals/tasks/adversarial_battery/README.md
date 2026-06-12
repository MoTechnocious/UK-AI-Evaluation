# adversarial_battery

Runs the **adversarial test battery v1** — 36 probes across six threat categories —
against a system under test and scores each PASS (resisted) / FAIL (compromised) with a
model grader, against each case's own `pass_criteria`.

Battery and full category/severity definitions:
[`evals/datasets/adversarial-battery-v1/`](../../datasets/adversarial-battery-v1/).
Design rationale: [ADR-003](../../../docs/adr/ADR-003-adversarial-battery.md).

**What it measures:** resistance to a fixed set of adversarial probes covering prompt
injection, jailbreak, data exfiltration, tool abuse, bias/fairness and clinical safety.
The headline metric is the pass-rate (`accuracy`) — the fraction of probes resisted.

**What it does NOT measure:** overall model safety, capability, or fitness for any
clinical purpose. The battery is a fixed probe set, not a guarantee — **passing is
necessary, not sufficient**. Never present a battery pass-rate as a safety certification.

## Running

```bash
# All categories. Use a grader independent of the target.
inspect eval evals/tasks/adversarial_battery/adversarial_battery.py \
  --model anthropic/claude-haiku-4-5-20251001 \
  -T grader_model=anthropic/claude-opus-4-8

# One category
inspect eval evals/tasks/adversarial_battery/adversarial_battery.py \
  -T category=clinical_safety --model <target>

# Quick smoke (first 3 cases)
inspect eval evals/tasks/adversarial_battery/adversarial_battery.py -T limit=3 --model <target>

inspect view   # browse the .eval log; every grade carries the grader's reasoning
```

Parameters: `category` (one of the six codes), `grader_model` (defaults to
`anthropic/claude-opus-4-8`), `limit`.

## Scoring notes

- **Model-graded.** Each case is graded against its `pass_criteria`; the grader's
  one-line justification is logged for audit. The parse is conservative — only an
  explicit `GRADE: PASS` counts as resisted, so ambiguous grades fail rather than
  silently pass.
- **Avoid self-grading.** Don't set `grader_model` to the same model under test; a
  model is a poor judge of its own compromise. Default grader differs from the example
  target on purpose.
- **Severity-weight in reporting, not here.** The scorer reports a flat pass-rate plus
  per-case severity in metadata; weight by severity when writing the report scorecard.
- The `.eval` log is the artefact of record — cite its ID against findings in the report.
