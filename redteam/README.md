# /redteam — Adversarial testing

Tooling standard: **garak**, **PyRIT**, **promptfoo**. Custom probes only when the
standard tools can't express the attack — and then as contributions structured so they
could be upstreamed.

## Layout

```
redteam/
  garak/        garak configs and custom probes
  pyrit/        PyRIT orchestrations and attack strategies
  promptfoo/    promptfoo configs (redteam + regression suites)
  findings/     structured findings awaiting promotion into a report (redacted)
```

## Taxonomy: OWASP LLM Top 10 (2025)

Every finding maps to at least one category so reports are legible to security buyers:

| ID | Category |
|---|---|
| LLM01 | Prompt Injection |
| LLM02 | Sensitive Information Disclosure |
| LLM03 | Supply Chain |
| LLM04 | Data and Model Poisoning |
| LLM05 | Improper Output Handling |
| LLM06 | Excessive Agency |
| LLM07 | System Prompt Leakage |
| LLM08 | Vector and Embedding Weaknesses |
| LLM09 | Misinformation |
| LLM10 | Unbounded Consumption |

## Rules of the room

- Red-team runs execute against **authorised targets only** — our own sandboxes, or a
  client system under a signed engagement that explicitly scopes the testing.
- Same reproducibility bar as `/evals`: pinned versions, captured configs, retained logs.
- Findings include severity, reproduction steps, OWASP mapping, and what was *not* probed.
