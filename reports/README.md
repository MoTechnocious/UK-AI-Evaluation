# /reports — AI Assurance Reports

The core deliverable: **evaluation scorecard → red-team findings → framework mapping**.

## Layout

```
reports/
  templates/    the canonical report skeleton and section templates
  published/    redacted, client-approved reports promoted into the open
                Assurance Evidence Base (nothing lands here without sign-off)
```

## Rules of the room

- Every claim in a report traces to an artefact in `/evals` or `/redteam` (run ID,
  `.eval` log, finding record). No artefact, no claim.
- Framework mappings reference the specific clause/control (ISO/IEC 42001, NIST AI RMF,
  EU AI Act high-risk requirements, OWASP LLM Top 10, DCB0129/0160 where clinical).
- Reports state scope and limitations as prominently as results.
- We are aligned with the direction of MHRA / UK AISI / NHS — reports never imply
  affiliation, certification or endorsement.
