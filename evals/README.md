# /evals — Evaluation harness

All evaluations are [Inspect](https://inspect.aisi.org.uk/) (UK AISI) tasks. A new
evaluation that isn't an Inspect task/solver/scorer needs an ADR explaining why.

## Layout

```
evals/
  tasks/<task-name>/      one directory per evaluation task
    <task>.py             the Inspect task (tasks, solvers, scorers)
    README.md             what it measures, dataset provenance, limitations
  datasets/               versioned datasets (synthetic/public/licensed ONLY —
                          provenance recorded; no real patient data, ever)
```

## Running

```bash
inspect eval evals/tasks/smoke/smoke.py --model anthropic/claude-haiku-4-5-20251001
inspect view   # browse the .eval logs
```

## Rules of the room

- The Inspect `.eval` log is the artefact of record — every reported score traces to one.
- Capture model ID, endpoint, parameters and seeds in the run; pin deps via the lockfile.
- Every task README states what it does **not** measure. Unstated limitations are
  overclaims, and overclaims are the one thing this company cannot ship.
