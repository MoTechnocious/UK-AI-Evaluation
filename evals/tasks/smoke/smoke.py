"""Smoke test task: proves the Inspect harness, provider keys and logging work
end-to-end. Not an assurance evaluation — it measures nothing about a model
beyond 'the pipe is connected'.

Run:
    inspect eval evals/tasks/smoke/smoke.py --model anthropic/claude-haiku-4-5-20251001
"""

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.scorer import exact
from inspect_ai.solver import generate


@task
def smoke() -> Task:
    return Task(
        dataset=[
            Sample(
                input="Reply with exactly the word OK and nothing else.",
                target="OK",
            )
        ],
        solver=generate(),
        scorer=exact(),
    )
