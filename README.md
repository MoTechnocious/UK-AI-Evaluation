# UK AI Assurance — Assurance Monorepo

Independent, audit-grade, reproducible AI assurance. We test, evaluate, red-team and
governance/compliance-map AI systems against safety, security, fairness, robustness and
regulatory expectations — health / clinical-diagnostics first.

This monorepo holds the assurance methodology and tooling behind the **AI Assurance
Report** (evaluation scorecard → adversarial red-team findings → framework mapping) and
the open **Assurance Evidence Base**.

> **Status:** pre-product R&D. Nothing here is a certified or accredited assessment.
> We are aligned with the direction of MHRA, UK AISI and the NHS — not affiliated with,
> certified by, or endorsed by any of them.

## Repository layout

| Path | What lives here |
|---|---|
| [`/evals`](evals/) | Inspect (UK AISI) evaluation tasks, solvers, scorers and datasets |
| [`/redteam`](redteam/) | Adversarial testing — garak, PyRIT, promptfoo configs and probe sets |
| [`/reports`](reports/) | AI Assurance Report templates and (redacted) published outputs |
| [`/infra`](infra/) | CI, runners, sandboxing and reproducibility plumbing |
| [`/docs`](docs/) | ADRs, methodology docs, framework mappings, runbooks |

## Tooling standard

- **Evaluation harness:** [Inspect](https://inspect.aisi.org.uk/) (UK AI Security Institute) — every evaluation is an Inspect task unless an ADR says otherwise.
- **Red-team:** [garak](https://github.com/NVIDIA/garak), [PyRIT](https://github.com/Azure/PyRIT), [promptfoo](https://www.promptfoo.dev/).
- **Taxonomy anchor:** [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — all red-team findings map to it.
- **Languages:** Python for evals/orchestration; Rust where determinism, performance or a hardened binary matters. Linux is the reference platform.

## Quickstart

```bash
# Python 3.11+ on Linux (reference platform)
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Run the smoke eval against a model you have keys for (keys go in .env, never in git)
cp .env.example .env   # then fill in
inspect eval evals/tasks/smoke/smoke.py --model anthropic/claude-haiku-4-5-20251001

# Lint and tests
ruff check . && ruff format --check . && pytest -q
```

## Reproducibility is the product

Every result in this repo must be re-runnable by a third party. That means, for every
run we report: pinned dependency versions (lockfile), the exact model ID and endpoint,
all generation parameters, seeds where the stack supports them, and the full input/output
log (Inspect's `.eval` log is the artefact of record). If a score can't be traced to the
artefact that produced it, it isn't assurance — it's an opinion.

## Security

No secrets in git — API keys live in `.env` (gitignored) or CI secrets. Treat all pilot
data as sensitive (clinical-adjacent bar). See [SECURITY.md](SECURITY.md).

## Licence

Not yet licensed — all rights reserved while the licensing decision is made
(see [docs/adr/ADR-002-licensing.md](docs/adr/ADR-002-licensing.md), status: proposed).

## Contact

UK AI Assurance — London, UK · <https://ukaiassurance.com> · inquiries@ukaiassurance.com
