import ast
from datetime import datetime, timezone
from pathlib import Path

import pytest
from pydantic import ValidationError

from domain.plan import Plan, PlanOutcome


PLAN_PATH = Path(__file__).parents[3] / "domain" / "plan.py"


def test_plan_outcome_has_expected_values() -> None:
    assert [(item.name, item.value) for item in PlanOutcome] == [
        ("PENDING", "pending"),
        ("COMPLETED", "completed"),
        ("FAILED", "failed"),
        ("SUPERSEDED", "superseded"),
        ("ABORTED", "aborted"),
    ]


def test_plan_is_structurally_valid() -> None:
    now = datetime.now(timezone.utc)
    plan = Plan(
        plan_id="plan-101",
        task_id="task-501",
        created_at=now,
        based_on=("fact-1", "fact-2"),
        assumptions=("device_is_online",),
        constraints=("max_retries=3",),
        validity_conditions=("battery_above_20",),
        intended_action="restart_service",
        supersedes="plan-99",
        superseded_by=None,
        outcome=PlanOutcome.PENDING,
    )

    assert plan.plan_id == "plan-101"
    assert plan.task_id == "task-501"
    assert plan.created_at == now
    assert plan.based_on == ("fact-1", "fact-2")
    assert plan.assumptions == ("device_is_online",)
    assert plan.constraints == ("max_retries=3",)
    assert plan.validity_conditions == ("battery_above_20",)
    assert plan.intended_action == "restart_service"
    assert plan.supersedes == "plan-99"
    assert plan.superseded_by is None
    assert plan.outcome == PlanOutcome.PENDING


def test_plan_is_frozen() -> None:
    plan = Plan(
        plan_id="plan-1",
        task_id="task-1",
        created_at=datetime.now(timezone.utc),
        intended_action="noop",
    )

    with pytest.raises(ValidationError):
        plan.plan_id = "plan-2"  # type: ignore[misc]

    with pytest.raises(ValidationError):
        plan.task_id = "task-2"  # type: ignore[misc]

    with pytest.raises(ValidationError):
        plan.outcome = PlanOutcome.COMPLETED  # type: ignore[misc]


def test_plan_uses_immutable_tuples() -> None:
    plan = Plan(
        plan_id="plan-1",
        task_id="task-1",
        created_at=datetime.now(timezone.utc),
        based_on=["f1", "f2"],  # type: ignore[arg-type]
        assumptions=["a1"],  # type: ignore[arg-type]
        constraints=["c1"],  # type: ignore[arg-type]
        validity_conditions=["v1"],  # type: ignore[arg-type]
        intended_action="do_something",
    )

    assert isinstance(plan.based_on, tuple)
    assert isinstance(plan.assumptions, tuple)
    assert isinstance(plan.constraints, tuple)
    assert isinstance(plan.validity_conditions, tuple)
    assert plan.based_on == ("f1", "f2")
    assert plan.assumptions == ("a1",)
    assert plan.constraints == ("c1",)
    assert plan.validity_conditions == ("v1",)


def test_task_reference_is_stored_as_id() -> None:
    plan = Plan(
        plan_id="plan-1",
        task_id="task-xyz-999",
        created_at=datetime.now(timezone.utc),
        intended_action="run",
    )

    assert isinstance(plan.task_id, str)
    assert plan.task_id == "task-xyz-999"


def test_plan_references_are_stored_as_ids() -> None:
    plan = Plan(
        plan_id="plan-10",
        task_id="task-1",
        created_at=datetime.now(timezone.utc),
        intended_action="run",
        supersedes="plan-9",
        superseded_by="plan-11",
    )

    assert plan.supersedes == "plan-9"
    assert plan.superseded_by == "plan-11"


def test_plan_does_not_execute_actions() -> None:
    plan = Plan(
        plan_id="plan-1",
        task_id="task-1",
        created_at=datetime.now(timezone.utc),
        intended_action="delete_database",
    )
    assert plan.intended_action == "delete_database"
    assert not hasattr(plan, "execute")
    assert not hasattr(plan, "run")


def test_plan_does_not_resolve_runtime_objects() -> None:
    plan = Plan(
        plan_id="plan-1",
        task_id="task-1",
        created_at=datetime.now(timezone.utc),
        based_on=("id-1", "id-2"),
        intended_action="action",
    )
    assert all(isinstance(x, str) for x in plan.based_on)


def test_no_forbidden_layer_imports() -> None:
    forbidden_imports = {
        "application",
        "infrastructure",
        "interface",
        "domain.capability",
        "domain.task",
        "domain.worldstate",
        "domain.authorization",
        "domain.policy",
        "domain.risk",
    }
    tree = ast.parse(PLAN_PATH.read_text(encoding="utf-8"))

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
    tree = ast.parse(PLAN_PATH.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            assert node.level == 0, f"Relative import detected: level={node.level}, module={node.module}"