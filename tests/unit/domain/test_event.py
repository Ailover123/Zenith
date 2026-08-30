import ast
from datetime import datetime, timezone
from pathlib import Path

import pytest
from pydantic import ValidationError

from domain.event import ObservationEvent


EVENT_PATH = Path(__file__).parents[3] / "domain" / "event.py"


def test_observation_event_is_structurally_valid() -> None:
    now = datetime.now(timezone.utc)
    event = ObservationEvent(
        event_id="evt-1001",
        source="gmail",
        source_native_id="msg-98765",
        event_type="message_received",
        timestamp=now,
        resource_key="mailbox:user@example.com",
        raw_payload={"headers": {"from": "alice@example.com"}, "body": "Hello"},
        normalized_payload={"sender": "alice@example.com", "preview": "Hello"},
        provenance="webhook:gmail-push",
        correlation_id="corr-abc-123",
    )

    assert event.event_id == "evt-1001"
    assert event.source == "gmail"
    assert event.source_native_id == "msg-98765"
    assert event.event_type == "message_received"
    assert event.timestamp == now
    assert event.resource_key == "mailbox:user@example.com"
    assert event.raw_payload == {"headers": {"from": "alice@example.com"}, "body": "Hello"}
    assert event.normalized_payload == {"sender": "alice@example.com", "preview": "Hello"}
    assert event.provenance == "webhook:gmail-push"
    assert event.correlation_id == "corr-abc-123"


def test_observation_event_is_frozen() -> None:
    now = datetime.now(timezone.utc)
    event = ObservationEvent(
        event_id="evt-1",
        source="github",
        source_native_id="deliv-42",
        event_type="push_event",
        timestamp=now,
        resource_key="repo:zenith",
        raw_payload={"ref": "refs/heads/main"},
        normalized_payload={"branch": "main"},
        provenance="webhook:github",
        correlation_id="corr-1",
    )

    with pytest.raises(ValidationError):
        event.event_id = "evt-2"  # type: ignore[misc]

    with pytest.raises(ValidationError):
        event.source = "gitlab"  # type: ignore[misc]

    with pytest.raises(ValidationError):
        event.raw_payload = {}  # type: ignore[misc]

    with pytest.raises(ValidationError):
        event.event_type = "pull_request"  # type: ignore[misc]


def test_event_id_is_stored_as_id() -> None:
    event = ObservationEvent(
        event_id="evt-uuid-001",
        source="calendar",
        source_native_id="cal-evt-1",
        event_type="event_created",
        timestamp=datetime.now(timezone.utc),
        resource_key="calendar:primary",
        raw_payload="raw-data",
        normalized_payload={"summary": "Meeting"},
        provenance="polling:calendar-sync",
        correlation_id="corr-1",
    )

    assert isinstance(event.event_id, str)
    assert event.event_id == "evt-uuid-001"


def test_source_native_id_is_stored_as_id() -> None:
    event = ObservationEvent(
        event_id="evt-1",
        source="calendar",
        source_native_id="cal-native-99",
        event_type="event_updated",
        timestamp=datetime.now(timezone.utc),
        resource_key="calendar:primary",
        raw_payload="raw-data",
        normalized_payload={"summary": "Updated Meeting"},
        provenance="polling:calendar-sync",
        correlation_id="corr-1",
    )

    assert isinstance(event.source_native_id, str)
    assert event.source_native_id == "cal-native-99"


def test_event_type_accepts_structurally_valid_identifier() -> None:
    valid_types = [
        "message_received",
        "file_uploaded_v2",
        "push",
        "user_login_session_started",
        "a",
    ]
    for vtype in valid_types:
        event = ObservationEvent(
            event_id="evt-1",
            source="system",
            source_native_id="nat-1",
            event_type=vtype,
            timestamp=datetime.now(timezone.utc),
            resource_key="res-1",
            raw_payload=None,
            normalized_payload={},
            provenance="system",
            correlation_id="corr-1",
        )
        assert event.event_type == vtype


def test_event_type_rejects_invalid_structure() -> None:
    invalid_types = [
        "",
        "MessageReceived",
        "message-received",
        "message received",
        "123_starts_with_digit",
        "_starts_with_underscore",
        "message.received",
        "message@received",
    ]
    for inv_type in invalid_types:
        with pytest.raises(ValidationError):
            ObservationEvent(
                event_id="evt-1",
                source="system",
                source_native_id="nat-1",
                event_type=inv_type,
                timestamp=datetime.now(timezone.utc),
                resource_key="res-1",
                raw_payload=None,
                normalized_payload={},
                provenance="system",
                correlation_id="corr-1",
            )


def test_timestamp_is_stored_as_advisory_metadata() -> None:
    now = datetime(2026, 8, 30, 12, 0, 0, tzinfo=timezone.utc)
    event = ObservationEvent(
        event_id="evt-1",
        source="sensor",
        source_native_id="reading-1",
        event_type="temperature_readable",
        timestamp=now,
        resource_key="device:sensor-1",
        raw_payload=22.5,
        normalized_payload={"temp_celsius": 22.5},
        provenance="mqtt:sensor",
        correlation_id="corr-1",
    )

    assert isinstance(event.timestamp, datetime)
    assert event.timestamp == now


def test_resource_key_is_stored_as_identifier() -> None:
    event = ObservationEvent(
        event_id="evt-1",
        source="filesystem",
        source_native_id="file-hash-123",
        event_type="file_modified",
        timestamp=datetime.now(timezone.utc),
        resource_key="file:///data/report.pdf",
        raw_payload={"path": "/data/report.pdf"},
        normalized_payload={"path": "/data/report.pdf"},
        provenance="inotify",
        correlation_id="corr-file-1",
    )

    assert isinstance(event.resource_key, str)
    assert event.resource_key == "file:///data/report.pdf"


def test_raw_payload_is_preserved() -> None:
    arbitrary_raw = {
        "nested": {"values": [1, 2, 3], "flag": True},
        "int": 42,
    }
    event = ObservationEvent(
        event_id="evt-1",
        source="custom",
        source_native_id="custom-1",
        event_type="custom_event",
        timestamp=datetime.now(timezone.utc),
        resource_key="custom:1",
        raw_payload=arbitrary_raw,
        normalized_payload={"status": "ok"},
        provenance="custom-source",
        correlation_id="corr-1",
    )

    assert event.raw_payload == arbitrary_raw


def test_normalized_payload_is_stored() -> None:
    normalized = {"field_a": "value_a", "count": 10}
    event = ObservationEvent(
        event_id="evt-1",
        source="custom",
        source_native_id="custom-1",
        event_type="custom_event",
        timestamp=datetime.now(timezone.utc),
        resource_key="custom:1",
        raw_payload="raw",
        normalized_payload=normalized,
        provenance="custom-source",
        correlation_id="corr-1",
    )

    assert isinstance(event.normalized_payload, dict)
    assert event.normalized_payload == normalized


def test_provenance_is_stored() -> None:
    event = ObservationEvent(
        event_id="evt-1",
        source="slack",
        source_native_id="slack-msg-1",
        event_type="channel_message",
        timestamp=datetime.now(timezone.utc),
        resource_key="slack:channel:general",
        raw_payload={"text": "hello"},
        normalized_payload={"text": "hello"},
        provenance="webhook:slack:bot-token",
        correlation_id="corr-slack-1",
    )

    assert isinstance(event.provenance, str)
    assert event.provenance == "webhook:slack:bot-token"


def test_correlation_id_is_stored() -> None:
    event = ObservationEvent(
        event_id="evt-1",
        source="slack",
        source_native_id="slack-msg-1",
        event_type="channel_message",
        timestamp=datetime.now(timezone.utc),
        resource_key="slack:channel:general",
        raw_payload={"text": "hello"},
        normalized_payload={"text": "hello"},
        provenance="webhook:slack:bot-token",
        correlation_id="flow-req-9999",
    )

    assert isinstance(event.correlation_id, str)
    assert event.correlation_id == "flow-req-9999"


def test_source_and_source_native_id_are_represented() -> None:
    event = ObservationEvent(
        event_id="evt-1",
        source="stripe",
        source_native_id="evt_1Nx3249",
        event_type="charge_succeeded",
        timestamp=datetime.now(timezone.utc),
        resource_key="customer:cus_123",
        raw_payload={"amount": 5000},
        normalized_payload={"amount_dollars": 50.0},
        provenance="webhook:stripe",
        correlation_id="corr-stripe-1",
    )

    assert event.source == "stripe"
    assert event.source_native_id == "evt_1Nx3249"


def test_no_external_state_is_required() -> None:
    event = ObservationEvent(
        event_id="evt-self-contained",
        source="local",
        source_native_id="local-0",
        event_type="local_event",
        timestamp=datetime.now(timezone.utc),
        resource_key="local:res",
        raw_payload={},
        normalized_payload={},
        provenance="internal",
        correlation_id="corr-0",
    )
    assert isinstance(event, ObservationEvent)


def test_no_forbidden_layer_imports() -> None:
    forbidden_imports = {
        "application",
        "infrastructure",
        "interface",
        "domain.worldstate",
        "domain.capability",
        "domain.policy",
        "domain.risk",
        "domain.scope",
        "domain.plan",
        "domain.task",
    }
    tree = ast.parse(EVENT_PATH.read_text(encoding="utf-8"))

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
    tree = ast.parse(EVENT_PATH.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            assert node.level == 0, f"Relative import detected: level={node.level}, module={node.module}"