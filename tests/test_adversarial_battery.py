"""CI checks for the adversarial battery: dataset is well-formed and the task
constructs, without calling any model."""

import importlib.util
import json
from collections import Counter
from pathlib import Path

from inspect_ai import Task

REPO_ROOT = Path(__file__).resolve().parents[1]
BATTERY = REPO_ROOT / "evals" / "datasets" / "adversarial-battery-v1" / "battery.jsonl"
TASK_PATH = REPO_ROOT / "evals" / "tasks" / "adversarial_battery" / "adversarial_battery.py"

REQUIRED_FIELDS = {
    "id",
    "category",
    "owasp",
    "technique",
    "severity",
    "input",
    "expected_behavior",
    "pass_criteria",
    "fail_signals",
}
CATEGORIES = {
    "prompt_injection",
    "jailbreak",
    "data_exfiltration",
    "tool_abuse",
    "bias_fairness",
    "clinical_safety",
}
SEVERITIES = {"critical", "high", "medium", "low"}


def _load_records():
    records = []
    with BATTERY.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def _load_task_module():
    spec = importlib.util.spec_from_file_location("adversarial_battery", TASK_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_dataset_parses_as_jsonl():
    records = _load_records()
    assert records, "battery.jsonl is empty"


def test_definition_of_done_counts():
    records = _load_records()
    # DoD: >=30 cases across 6 categories, >=5 per category.
    assert len(records) >= 30, f"expected >=30 cases, got {len(records)}"
    by_cat = Counter(r["category"] for r in records)
    assert set(by_cat) == CATEGORIES, f"unexpected categories: {set(by_cat)}"
    for cat in CATEGORIES:
        assert by_cat[cat] >= 5, f"category {cat} has only {by_cat[cat]} cases (need >=5)"


def test_every_case_is_well_formed():
    records = _load_records()
    for r in records:
        missing = REQUIRED_FIELDS - set(r)
        assert not missing, f"{r.get('id', '?')} missing fields: {missing}"
        assert r["severity"] in SEVERITIES, f"{r['id']} bad severity {r['severity']}"
        assert r["category"] in CATEGORIES, f"{r['id']} bad category {r['category']}"
        assert isinstance(r["owasp"], list) and r["owasp"], f"{r['id']} owasp must be non-empty list"
        assert isinstance(r["fail_signals"], list), f"{r['id']} fail_signals must be a list"
        # Every case must carry a severity and an expected-pass definition (the AC).
        assert r["pass_criteria"].strip(), f"{r['id']} empty pass_criteria"
        assert r["input"].strip(), f"{r['id']} empty input"


def test_ids_are_unique():
    records = _load_records()
    ids = [r["id"] for r in records]
    dupes = [i for i, n in Counter(ids).items() if n > 1]
    assert not dupes, f"duplicate ids: {dupes}"


def test_task_constructs_all_categories():
    module = _load_task_module()
    t = module.adversarial_battery()
    assert isinstance(t, Task)
    assert len(list(t.dataset)) >= 30


def test_task_constructs_filtered_by_category():
    module = _load_task_module()
    t = module.adversarial_battery(category="clinical_safety")
    samples = list(t.dataset)
    assert samples, "category filter returned no samples"
    assert all(s.metadata["category"] == "clinical_safety" for s in samples)


def test_unknown_category_rejected():
    module = _load_task_module()
    try:
        module.adversarial_battery(category="not_a_category")
    except ValueError:
        return
    raise AssertionError("expected ValueError for unknown category")
