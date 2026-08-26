import ast
from pathlib import Path

import pytest
from pydantic import ValidationError

from domain.authorization import (
    DecisionObject,
    DelegationScope,
    RootGrant,
    Verdict,
)


AUTHORIZATION_PATH = Path(__file__).parents[3] / "domain" / "authorization.py"


def test_verdict_has_expected_values() -> None:
    assert [(item.name, item.value) for item in Verdict] == [
        ("ALLOW", "allow"),
        ("DENY", "deny"),
        ("REQUIRE_APPROVAL", "require_approval"),
        ("SECURITY_UNAVAILABLE", "security_unavailable"),
        ("THROTTLED", "throttled"),
    ]


def test_decision_object_is_structurally_valid() -> None:
    decision = DecisionObject(
        id="dec-1",
        subject_id="sub-1",
        capability_id="cap-1",
        verdict=Verdict.ALLOW,
        reason="Action permitted by policy",
    )

    assert decision.id == "dec-1"
    assert decision.subject_id == "sub-1"
    assert decision.capability_id == "cap-1"
    assert decision.verdict is Verdict.ALLOW
    assert decision.reason == "Action permitted by policy"


def test_decision_object_is_frozen() -> None:
    decision = DecisionObject(
        id="dec-1",
        subject_id="sub-1",
        capability_id="cap-1",
        verdict=Verdict.ALLOW,
        reason="Action permitted",
    )

    with pytest.raises(ValidationError):
        decision.verdict = Verdict.DENY  # type: ignore[misc]


def test_decision_object_requires_subject_id() -> None:
    with pytest.raises(ValidationError):
        DecisionObject(  # type: ignore[call-arg]
            id="dec-1",
            capability_id="cap-1",
            verdict=Verdict.ALLOW,
            reason="Action permitted",
        )


def test_decision_object_requires_capability_id() -> None:
    with pytest.raises(ValidationError):
        DecisionObject(  # type: ignore[call-arg]
            id="dec-1",
            subject_id="sub-1",
            verdict=Verdict.ALLOW,
            reason="Action permitted",
        )


def test_decision_object_requires_reason() -> None:
    with pytest.raises(ValidationError):
        DecisionObject(  # type: ignore[call-arg]
            id="dec-1",
            subject_id="sub-1",
            capability_id="cap-1",
            verdict=Verdict.ALLOW,
        )


def test_root_grant_is_structurally_valid() -> None:
    grant = RootGrant(
        id="grant-1",
        subject_id="sub-1",
        capability_id="cap-1",
    )

    assert grant.id == "grant-1"
    assert grant.subject_id == "sub-1"
    assert grant.capability_id == "cap-1"
    assert grant.scope is None


def test_root_grant_is_frozen() -> None:
    grant = RootGrant(
        id="grant-1",
        subject_id="sub-1",
        capability_id="cap-1",
    )

    with pytest.raises(ValidationError):
        grant.capability_id = "cap-2"  # type: ignore[misc]


def test_root_grant_requires_subject_id() -> None:
    with pytest.raises(ValidationError):
        RootGrant(  # type: ignore[call-arg]
            id="grant-1",
            capability_id="cap-1",
        )


def test_root_grant_requires_capability_id() -> None:
    with pytest.raises(ValidationError):
        RootGrant(  # type: ignore[call-arg]
            id="grant-1",
            subject_id="sub-1",
        )


def test_delegation_scope_is_structurally_valid() -> None:
    scope = DelegationScope(
        capability_ids=("cap-1", "cap-2"),
        subject_ids=("sub-1", "sub-2"),
    )

    assert scope.capability_ids == ("cap-1", "cap-2")
    assert scope.subject_ids == ("sub-1", "sub-2")


def test_delegation_scope_defaults_to_unrestricted_dimensions() -> None:
    scope = DelegationScope()

    assert scope.capability_ids == ()
    assert scope.subject_ids == ()


def test_delegation_scope_is_frozen() -> None:
    scope = DelegationScope()

    with pytest.raises(ValidationError):
        scope.capability_ids = ("cap-1",)  # type: ignore[misc]


def test_delegation_scope_accepts_capability_ids() -> None:
    scope = DelegationScope(capability_ids=("cap-read", "cap-write"))
    assert scope.capability_ids == ("cap-read", "cap-write")
    assert scope.subject_ids == ()


def test_delegation_scope_accepts_subject_ids() -> None:
    scope = DelegationScope(subject_ids=("sub-agent-1", "sub-agent-2"))
    assert scope.capability_ids == ()
    assert scope.subject_ids == ("sub-agent-1", "sub-agent-2")


def test_allow_verdict_is_representable() -> None:
    decision = DecisionObject(
        id="dec-allow",
        subject_id="sub-1",
        capability_id="cap-1",
        verdict=Verdict.ALLOW,
        reason="Permitted",
    )
    assert decision.verdict is Verdict.ALLOW


def test_deny_verdict_is_representable() -> None:
    decision = DecisionObject(
        id="dec-deny",
        subject_id="sub-1",
        capability_id="cap-1",
        verdict=Verdict.DENY,
        reason="Denied by policy",
    )
    assert decision.verdict is Verdict.DENY


def test_require_approval_verdict_is_representable() -> None:
    decision = DecisionObject(
        id="dec-appr",
        subject_id="sub-1",
        capability_id="cap-1",
        verdict=Verdict.REQUIRE_APPROVAL,
        reason="High risk requires human approval",
    )
    assert decision.verdict is Verdict.REQUIRE_APPROVAL


def test_security_unavailable_verdict_is_representable() -> None:
    decision = DecisionObject(
        id="dec-sec-unavail",
        subject_id="sub-1",
        capability_id="cap-1",
        verdict=Verdict.SECURITY_UNAVAILABLE,
        reason="Security service unreachable",
    )
    assert decision.verdict is Verdict.SECURITY_UNAVAILABLE


def test_throttled_verdict_is_representable() -> None:
    decision = DecisionObject(
        id="dec-throttled",
        subject_id="sub-1",
        capability_id="cap-1",
        verdict=Verdict.THROTTLED,
        reason="Rate limit exceeded",
    )
    assert decision.verdict is Verdict.THROTTLED


def test_no_forbidden_layer_imports() -> None:
    forbidden_imports = {
        "application",
        "infrastructure",
        "interface",
        "domain.capability",
        "domain.policy",
        "domain.risk",
    }
    tree = ast.parse(AUTHORIZATION_PATH.read_text(encoding="utf-8"))

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
