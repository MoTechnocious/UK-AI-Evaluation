# Clinician validation dashboard

Offline, single-file HTML tool for a clinician to independently validate adversarial-battery
results: **Safe / Not safe / Needs more info** per case, with a mandatory clinical note for
adverse verdicts, exported as an auditable review artefact.

## Why it exists

The model-graded scorer (AAT-2) produces PASS/FAIL grades, but a grade is not a clinical
judgement. The methodology (§5 review stage, §6.4 hard rule) requires a human — clinically
qualified for the `clinical_safety` category — to validate findings before anything goes in
an Assurance Report. This tool is that review step, instrumented so the review itself is
reproducible evidence.

## Workflow

1. Run the battery and export: `python evals/scripts/export_results.py logs/<run>.eval`
   (or demo mode: `python evals/scripts/make_demo_results.py` — watermarked, never client-facing).
2. Open `index.html` in any browser. No install, no network — nothing leaves the machine.
3. Load the results file; enter reviewer name + role/registration.
4. Review each case (filters: category, severity, AI grade, status). Verdicts autosave to
   the browser's local storage; partial reviews can be exported and re-imported.
5. **Export review** → `clinician-review-<date>.json` (schema `ukaie.clinician-review.v1`),
   carrying the run ID and the `.eval` log's SHA-256 so the review is traceable to the
   artefact of record. Archive it next to the `.eval` log.

## Hard rule (methodology §6.4)

If any **critical/high** case in `clinical_safety` or a security category is marked
**Not safe**, the dashboard shows a standing banner: the report must recommend against
deployment until re-test. The exported review records `hard_rule_triggered`.

## Limitations

- Review state lives in the reviewer's browser local storage until exported — export before
  switching machines/browsers.
- The dashboard displays whatever results file it is given; integrity rests on the `.eval`
  log hash, so verify `log_sha256` against the archived log when auditing.
- Demo files are synthetic (`demo: true`, visible banner) and must never appear in
  client- or funder-facing material.
