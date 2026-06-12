"""Export an Inspect .eval log to the clinician-review dashboard format.

Reads the .eval log produced by running the adversarial battery and writes a
self-contained ``results.json`` (schema ``ukaie.results.v1``) that
``reports/clinician-review/index.html`` can load.

Usage:
    python evals/scripts/export_results.py logs/<run>.eval -o reports/clinician-review/results.json

Requires: inspect-ai (already a project dependency for running evals).
The .eval log remains the artefact of record (ADR-001); this export is a
derived view for clinical review and must not replace the log.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = "ukaie.results.v1"


def export(log_path: Path, out_path: Path) -> dict:
    try:
        from inspect_ai.log import read_eval_log
    except ImportError:
        sys.exit("inspect-ai is not installed. Run: pip install inspect-ai")

    log = read_eval_log(str(log_path))
    if log.status != "success":
        print(f"WARNING: log status is {log.status!r}, not 'success'", file=sys.stderr)

    results = []
    for sample in log.samples or []:
        meta = sample.metadata or {}
        score = None
        if sample.scores:
            # scorer is named 'resisted'
            score = sample.scores.get("resisted") or next(iter(sample.scores.values()))
        grade = "UNGRADED"
        explanation = ""
        response = ""
        if score is not None:
            grade = "PASS" if score.value in ("C", 1, 1.0, True) else "FAIL"
            explanation = score.explanation or ""
            response = score.answer or ""
        if not response and sample.output:
            response = sample.output.completion or ""
        results.append(
            {
                "id": sample.id,
                "category": meta.get("category", ""),
                "owasp": meta.get("owasp", ""),
                "technique": meta.get("technique", ""),
                "severity": meta.get("severity", ""),
                "input": meta.get("input", sample.input if isinstance(sample.input, str) else ""),
                "expected_behavior": meta.get("expected_behavior", ""),
                "pass_criteria": meta.get("pass_criteria", ""),
                "response": response,
                "grade": grade,
                "grader_explanation": explanation,
            }
        )

    log_bytes = Path(log_path).read_bytes()
    payload = {
        "schema": SCHEMA,
        "run": {
            "demo": False,
            "run_id": getattr(log.eval, "run_id", "") or "",
            "task": getattr(log.eval, "task", "") or "adversarial_battery",
            "battery_version": "adversarial-battery-v1",
            "target_model": getattr(log.eval, "model", "") or "",
            "grader_model": str((getattr(log.eval, "task_args", None) or {}).get("grader_model", "")),
            "created": str(getattr(log.eval, "created", "")) or datetime.now(timezone.utc).isoformat(),
            "exported_at": datetime.now(timezone.utc).isoformat(),
            "log_file": str(log_path),
            "log_sha256": hashlib.sha256(log_bytes).hexdigest(),
            "total": len(results),
            "passed": sum(1 for r in results if r["grade"] == "PASS"),
            "failed": sum(1 for r in results if r["grade"] == "FAIL"),
        },
        "results": results,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return payload


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("log", type=Path, help="path to the .eval log file")
    ap.add_argument(
        "-o",
        "--out",
        type=Path,
        default=Path("reports/clinician-review/results.json"),
        help="output path (default: reports/clinician-review/results.json)",
    )
    args = ap.parse_args()
    payload = export(args.log, args.out)
    run = payload["run"]
    print(
        f"Exported {run['total']} cases ({run['passed']} PASS / {run['failed']} FAIL) "
        f"-> {args.out}\nlog sha256: {run['log_sha256']}"
    )


if __name__ == "__main__":
    main()
