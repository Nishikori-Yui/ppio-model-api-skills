from __future__ import annotations

from ..specs import operation

OPERATIONS = (
    operation(
        group="tasks",
        family="async",
        name="async-task-result",
        title="查询任务结果",
        method="GET",
        base="v3",
        path="/async/task-result",
        doc_slug="reference-get-async-task-result",
        explicit_intent=False,
    ),
)
