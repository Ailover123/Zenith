import ast
from datetime import datetime, timezone
from pathlib import Path

import pytest
from pydantic import ValidationError

from domain.scope import DomainScope
from domain.task import ResumeTrigger, Task, TaskEvent, TaskStatus


FILE_PATH = Path(__file__).parents[3] / "domain" / "task.py"


def test_task_status_has_expected_values() -> None:
    assert [(item.name, item.value) for item in TaskStatus] == [
        ("CREATED", "created"),
        ("OBSERVING", "observing"),
        ("PLANNING", "planning"),
        ("REVALIDATING", "revalidating"),
        ("ACTING", "acting"),
        ("WAITING", "waiting"),
        ("DELEGATED", "delegated"),
        ("ASKING", "asking"),
        ("SURFACED", "surfaced"),
        ("COMPLETED", "completed"),
        ("FAILED", "failed"),
        ("ESCALATED_TO_HUMAN", "escalated_to_human"),
    ]


def test_resume_trigger_is_structurally_valid() -> None:
    trigger = ResumeTrigger(
        trigger_type="time_elapsed",
        configuration={"timeout_seconds": 60},
    )
    assert trigger.trigger_type == "time_elapsed"
    assert trigger.configuration == {"timeout_seconds": 60}


def test_resume_trigger_is_frozen() -> None:
    trigger = ResumeTrigger(trigger_type="time_elapsed")
    with pytest.raises(ValidationError):
        trigger.trigger_type = "event_received"  # type: ignore[misc]


def test_resume_trigger_rejects_invalid_trigger_type() -> None:
    invalid_types = ["", "TimeElapsed", "time-elapsed", "time elapsed", "123_type"]
    for it in invalid_types:
        with pytest.raises(ValidationError):
            ResumeTrigger(trigger_type=it)


def test_task_event_is_structurally_valid() -> None:
    now = datetime.now(timezone.utc)
    event = TaskEvent(
        event_id="evt-1",
        task_id="task-1",
        event_type="task_created",
        timestamp=now,
        details={"reason": "initial"},
    )
    assert event.event_id == "evt-1"
    assert event.task_id == "task-1"
    assert event.event_type == "task_created"
    assert event.timestamp == now
    assert event.details == {"reason": "initial"}


def test_task_event_is_frozen() -> None:
    event = TaskEvent(
        event_id="evt-1",
        task_id="task-1",
        event_type="task_created",
        timestamp=datetime.now(timezone.utc),
    )
    with pytest.raises(ValidationError):
        event.event_id = "evt-2"  # type: ignore[misc]


def test_task_event_rejects_invalid_event_type() -> None:
    invalid_types = ["", "TaskCreated", "task-created", "task created", "123_task"]
    for it in invalid_types:
        with pytest.raises(ValidationError):
            TaskEvent(
                event_id="evt-1",
                task_id="task-1",
                event_type=it,
                timestamp=datetime.now(timezone.utc),
            )


def test_task_is_structurally_valid() -> None:
    now = datetime.now(timezone.utc)
    scope = DomainScope(allowed_domains=("finance",))
    trigger = ResumeTrigger(trigger_type="user_input")
    task = Task(
        task_id="task-101",
        scope=scope,
        status=TaskStatus.PLANNING,
        created_at=now,
        parent_task_id="task-99",
        plan_id="plan-1",
        capability_id="cap-1",
        resume_trigger=trigger,
    )
    assert task.task_id == "task-101"
    assert task.scope == scope
    assert task.status == TaskStatus.PLANNING
    assert task.created_at == now
    assert task.parent_task_id == "task-99"
    assert task.plan_id == "plan-1"
    assert task.capability_id == "cap-1"
    assert task.resume_trigger == trigger


def test_task_defaults_status_to_created() -> None:
    task = Task(
        task_id="task-1",
        created_at=datetime.now(timezone.utc),
    )
    assert task.status == TaskStatus.CREATED
    assert task.parent_task_id is None
    assert task.plan_id is None
    assert task.capability_id is None
    assert task.resume_trigger is None


def test_task_is_frozen() -> None:
    task = Task(
        task_id="task-1",
        created_at=datetime.now(timezone.utc),
    )
    with pytest.raises(ValidationError):
        task.task_id = "task-2"  # type: ignore[misc]
    with pytest.raises(ValidationError):
        task.status = TaskStatus.ACTING  # type: ignore[misc]


def test_task_scope_uses_domain_scope() -> None:
    scope = DomainScope(allowed_entity_types=("user",))
    task = Task(
        task_id="task-1",
        scope=scope,
        created_at=datetime.now(timezone.utc),
    )
    assert isinstance(task.scope, DomainScope)
    assert task.scope.allowed_entity_types == ("user",)


def test_task_references_are_stored_as_ids() -> None:
    task = Task(
        task_id="task-101",
        created_at=datetime.now(timezone.utc),
        parent_task_id="parent-1",
        plan_id="plan-1",
        capability_id="cap-1",
    )
    assert isinstance(task.parent_task_id, str)
    assert isinstance(task.plan_id, str)
    assert isinstance(task.capability_id, str)


def test_optional_references_default_to_none() -> None:
    task = Task(
        task_id="task-1",
        created_at=datetime.now(timezone.utc),
    )
    assert task.parent_task_id is None
    assert task.plan_id is None
    assert task.capability_id is None
    assert task.resume_trigger is None


def test_resume_trigger_does_not_evaluate_conditions() -> None:
    trigger = ResumeTrigger(trigger_type="event_match", configuration={"event_id": "x"})
    assert not hasattr(trigger, "evaluate")
    assert not hasattr(trigger, "check")


def test_task_does_not_execute_capabilities() -> None:
    task = Task(
        task_id="task-1",
        created_at=datetime.now(timezone.utc),
        capability_id="cap-1",
    )
    assert not hasattr(task, "execute")
    assert not hasattr(task, "run")


def test_task_does_not_resolve_runtime_objects() -> None:
    task = Task(
        task_id="task-1",
        created_at=datetime.now(timezone.utc),
        plan_id="plan-1",
    )
    assert task.plan_id == "plan-1"
    assert isinstance(task.plan_id, str)


def test_no_forbidden_layer_imports() -> None:
    forbidden_imports = {
        "application",
        "infrastructure",
        "interface",
        "domain.capability",
        "domain.authorization",
        "domain.policy",
        "domain.risk",
        "domain.worldstate",
        "domain.event",
        "domain.plan",
    }
    tree = ast.parse(FILE_PATH.read_text(encoding="utf-8"))

    for import_node in ast.walk(tree):
        if isinstance(import_node, ast.Import):
            imported_names = {alias.name for alias in import_node.names}
        elif isinstance(import_node, ast.ImportFrom):
            assert import_node.level == 0, "relative imports are not permitted"
            imported_names = {import_node.module or ""}
        else:
            continue

        assert all(
            imported_name != forbidden_import
            and not imported_name.startswith(f"{forbidden_import}.")
            for imported_name in imported_names
            for forbidden_import in forbidden_imports
        )


def test_no_relative_imports() -> None:
    tree = ast.parse(FILE_PATH.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            assert node.level == 0, f"Relative import detected: level={node.level}, module={node.module}"
