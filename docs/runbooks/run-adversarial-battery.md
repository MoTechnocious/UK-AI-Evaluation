# Runbook — Run the adversarial battery v1 end-to-end

**Audience:** MZ / Mohamed. **Time:** ~30 min first run. **Cost:** see §5.
**Outcome:** a graded 36-case run, an auditable `.eval` log, a `results.json`, and a clinician review pack.

This is the full loop: run evals → export results → clinician validates safe/not-safe in the dashboard → archive both artefacts.

---

## 1. Prerequisites (once)

Linux/WSL or macOS recommended (Inspect works on Windows too).

```bash
git clone https://github.com/MoTechnocious/UK-AI-Evaluation && cd UK-AI-Evaluation
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]" && pip install inspect-ai
```

**Note (2026-06-12):** the battery lives on branch `feat/adversarial-battery-v1` until its PR is merged — `git checkout feat/adversarial-battery-v1` first. Open the PR at:
`https://github.com/MoTechnocious/UK-AI-Evaluation/pull/new/feat/adversarial-battery-v1`

## 2. API keys — never commit these

```bash
cp .env.example .env   # then edit .env
# ANTHROPIC_API_KEY=...   (target and/or grader)
# OPENAI_API_KEY=...      (if the target is an OpenAI model)
export $(grep -v '^#' .env | xargs)   # or use direnv
```

`.env` is gitignored. Check with `git status` before any commit. If a key is ever committed: revoke it immediately, then rewrite history.

## 3. Smoke run first (3 cases, ~£0.10)

```bash
inspect eval evals/tasks/adversarial_battery/adversarial_battery.py \
  --model anthropic/claude-haiku-4-5-20251001 \
  -T grader_model=anthropic/claude-opus-4-8 \
  -T limit=3
```

Check: run completes, log written to `./logs/`, and `inspect view` shows 3 graded samples with grader reasoning. **Spot-check the grades by hand** — the model-graded scorer has not yet been validated against human judgement (AAT-2 handoff §4c).

## 4. Full run (36 cases)

```bash
inspect eval evals/tasks/adversarial_battery/adversarial_battery.py \
  --model <target-model> \
  -T grader_model=anthropic/claude-opus-4-8 \
  --seed 42 --temperature 0
```

Rules of the house (reproducibility is the product):

- Pin everything: record target model string, grader model string, seed, temperature, `inspect_ai` version (`pip show inspect-ai`), battery version (v1), git commit.
- The `.eval` log in `./logs/` is the **artefact of record** (ADR-001). Never delete it; copy it to `reports/` evidence storage for any engagement.
- One category only: add `-T category=clinical_safety` (valid: `prompt_injection`, `jailbreak`, `data_exfiltration`, `tool_abuse`, `bias_fairness`, `clinical_safety`).
- Grader must be **independent of the target** (don't grade a model with itself).

## 5. Cost estimate (check current pricing before large runs)

36 cases ≈ 36 target calls + 36 grader calls, short prompts (<1k tokens each). With a Haiku-class target and Opus-class grader, expect **single-digit pounds per full run** at mid-2025 pricing; verify against current rate cards before committing to repeated runs. *API spend is Mohamed's call — confirm before first paid run.*

## 6. Export for clinician review

```bash
python evals/scripts/export_results.py logs/<your-run>.eval \
  -o reports/clinician-review/results.json
```

Note the printed `log sha256` — it ties the dashboard view back to the artefact of record.

## 7. Clinician validation

1. Open `reports/clinician-review/index.html` in any browser (works offline, no install).
2. Load `results.json` via the **Load results** button.
3. Reviewer enters name + role, then for each case records **Safe / Not safe / Needs more info** + a note. The AI grade is shown but the clinician's verdict is independent — disagreement is signal, not error.
4. **Export review** produces `clinician-review-<date>.json` (schema `ukaie.clinician-review.v1`). Store it next to the `.eval` log.

Per methodology §6: any Critical/High finding the clinician marks **Not safe** in `clinical_safety` or a security category ⇒ the report recommends against deployment until re-test.

## 8. No API key yet? Demo mode

```bash
python evals/scripts/make_demo_results.py
```

Writes `reports/clinician-review/results.demo.json` — fully synthetic, watermarked `demo: true`, banner shown in the dashboard. **Never** use demo artefacts in anything client- or funder-facing.

## 9. Troubleshooting

| Symptom | Fix |
|---|---|
| `inspect: command not found` | venv not active, or `pip install inspect-ai` |
| Auth error | key not exported into the shell; re-run the export line in §2 |
| `unknown category` | typo — see §4 list |
| Stale `.git/index.lock` (Windows working copy) | close editors/pause OneDrive sync, then `del .git\index.lock` |
| Grades look wrong | conservative parse means ambiguous → FAIL by design; spot-check with `inspect view` and record disagreements |

## 10. Limitations (state these in any report)

- 36 cases across 6 categories is a v1 screen, not coverage: no statistical claims from 6-case categories (methodology §9).
- Robustness (T3) has no suite yet; Governance (T6) is non-empirical.
- The model-graded scorer's agreement with human judgement is **not yet measured** — do that before relying on it in a paid engagement.
