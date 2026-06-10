"""CI check that the smoke task loads and is well-formed, without calling a model."""

import importlib.util
from pathlib import Path

from inspect_ai import Task

REPO_ROOT = Path(__file__).resolve().parents[1]
SMOKE_PATH = REPO_ROOT / "evals" / "tasks" / "smoke" / "smoke.py"


def _load_smoke_module():
    spec = importlib.util.spec_from_file_location("smoke", SMOKE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_smoke_task_constructs():
    module = _load_smoke_module()
    t = module.smoke()
    assert isinstance(t, Task)


def test_smoke_task_has_one_sample_with_target():
    module = _load_smoke_module()
    t = module.smoke()
    samples = list(t.dataset)
    assert len(samples) == 1
    assert samples[0].target == "OK"
