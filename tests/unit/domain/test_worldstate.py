import ast
from pathlib import Path

import pytest
from pydantic import ValidationError

from domain.worldstate import EntityType, WorldStateEntity


WORLDSTATE_PATH = Path(__file__).parents[3] / "domain" / "worldstate.py"


def test_entity_type_has_expected_values() -> None:
    assert [(item.name, item.value) for item in EntityType] == [
        ("USER", "user"),
        ("DEVICE", "device"),
        ("SERVICE", "service"),
        ("RESOURCE", "resource"),
        ("DOCUMENT", "document"),
        ("SYSTEM", "system"),
    ]


def test_world_state_entity_is_structurally_valid() -> None:
    entity = WorldStateEntity(
        entity_id="device-101",
        entity_type=EntityType.DEVICE,
        current_state={"status": "online", "battery": 95},
        state_version=1,
        last_updated_event_id="event-501",
    )

    assert entity.entity_id == "device-101"
    assert entity.entity_type is EntityType.DEVICE
    assert entity.current_state == {"status": "online", "battery": 95}
    assert entity.state_version == 1
    assert entity.last_updated_event_id == "event-501"


def test_world_state_entity_is_frozen() -> None:
    entity = WorldStateEntity(
        entity_id="user-1",
        entity_type=EntityType.USER,
        current_state={"role": "admin"},
        state_version=0,
        last_updated_event_id="event-1",
    )

    with pytest.raises(ValidationError):
        entity.entity_id = "user-2"  # type: ignore[misc]

    with pytest.raises(ValidationError):
        entity.state_version = 1  # type: ignore[misc]

    with pytest.raises(ValidationError):
        entity.current_state = {"role": "guest"}  # type: ignore[misc]


def test_state_version_must_be_non_negative() -> None:
    with pytest.raises(ValidationError):
        WorldStateEntity(
            entity_id="service-1",
            entity_type=EntityType.SERVICE,
            current_state={},
            state_version=-1,
            last_updated_event_id="event-1",
        )

    # state_version = 0 is valid (non-negative)
    entity = WorldStateEntity(
        entity_id="service-1",
        entity_type=EntityType.SERVICE,
        current_state={},
        state_version=0,
        last_updated_event_id="event-1",
    )
    assert entity.state_version == 0


def test_current_state_is_represented_as_mapping() -> None:
    state_payload = {"cpu_usage": 45.2, "active_sessions": 3, "tags": ["prod", "us-east"]}
    entity = WorldStateEntity(
        entity_id="system-1",
        entity_type=EntityType.SYSTEM,
        current_state=state_payload,
        state_version=2,
        last_updated_event_id="event-99",
    )

    assert isinstance(entity.current_state, dict)
    assert entity.current_state["cpu_usage"] == 45.2
    assert entity.current_state["active_sessions"] == 3
    assert entity.current_state["tags"] == ["prod", "us-east"]


def test_event_reference_is_stored_as_id() -> None:
    entity = WorldStateEntity(
        entity_id="doc-12",
        entity_type=EntityType.DOCUMENT,
        current_state={"title": "Spec"},
        state_version=4,
        last_updated_event_id="evt-abc-123",
    )

    assert isinstance(entity.last_updated_event_id, str)
    assert entity.last_updated_event_id == "evt-abc-123"


def test_entity_id_is_stored_as_id() -> None:
    entity = WorldStateEntity(
        entity_id="res-42",
        entity_type=EntityType.RESOURCE,
        current_state={"available": True},
        state_version=1,
        last_updated_event_id="evt-init",
    )

    assert isinstance(entity.entity_id, str)
    assert entity.entity_id == "res-42"


def test_no_forbidden_layer_imports() -> None:
    forbidden_imports = {
        "application",
        "infrastructure",
        "interface",
        "domain.event",
        "domain.authorization",
        "domain.capability",
        "domain.policy",
        "domain.risk",
        "domain.scope",
    }
    tree = ast.parse(WORLDSTATE_PATH.read_text(encoding="utf-8"))

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
    tree = ast.parse(WORLDSTATE_PATH.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            assert node.level == 0, f"Relative import detected: level={node.level}, module={node.module}"
