import ast
from pathlib import Path

import pytest
from pydantic import ValidationError

from domain.capability import Capability, CapabilityTemplate, ConstraintScope
from domain.policy import Policy, PolicyStatus, PolicyVerdict
from domain.risk import Risk, RiskLevel, RiskMode
from domain.vocabulary import Interface, Operation


CAPABILITY_PATH = Path(__file__).parents[3] / "domain" / "capability.py"


def _policy(
    *,
    verdict: PolicyVerdict = PolicyVerdict.ALLOW,
    status: PolicyStatus = PolicyStatus.ACTIVE,
    reviewed_by_human: bool = True,
) -> Policy:
    return Policy(
        id="policy-1",
        platform="platform-1",
        operation=Operation.EXECUTE,
        interface=Interface.API,
        verdict=verdict,
        status=status,
        version=1,
        reviewed_by_human=reviewed_by_human,
    )


def _risk(
    *,
    id: str = "risk-1",
    level: RiskLevel = RiskLevel.LOW,
    mode: RiskMode = RiskMode.EXPLICIT,
) -> Risk:
    return Risk(
        id=id,
        level=level,
        mode=mode,
    )


def _capability(
    *,
    id: str = "cap-1",
    template_id: str = "tpl-1",
    platform: str = "platform-1",
    operation: Operation = Operation.EXECUTE,
    interface: Interface = Interface.API,
    policy: Policy | None = None,
    risk: Risk | None = None,
    scope: ConstraintScope | None = None,
    requires_approval: bool = False,
    active: bool = True,
) -> Capability:
    return Capability(
        id=id,
        template_id=template_id,
        platform=platform,
        operation=operation,
        interface=interface,
        policy=policy if policy is not None else _policy(),
        risk=risk if risk is not None else _risk(),
        scope=scope if scope is not None else ConstraintScope(),
        requires_approval=requires_approval,
        active=active,
    )


def _assert_rejected(**kwargs: object) -> None:
    with pytest.raises(ValueError):
        _capability(**kwargs)


def test_capability_template_is_structurally_valid() -> None:
    template = CapabilityTemplate(
        id="tpl-1",
        name="Execute API Template",
        operation=Operation.EXECUTE,
        interface=Interface.API,
    )

    assert template.id == "tpl-1"
    assert template.name == "Execute API Template"
    assert template.operation is Operation.EXECUTE
    assert template.interface is Interface.API


def test_capability_template_is_frozen() -> None:
    template = CapabilityTemplate(
        id="tpl-1",
        name="Execute API Template",
        operation=Operation.EXECUTE,
        interface=Interface.API,
    )

    with pytest.raises(ValidationError):
        template.name = "Modified Template"  # type: ignore[misc]


def test_constraint_scope_is_structurally_valid() -> None:
    scope = ConstraintScope(
        platforms=("platform-1",),
        operations=(Operation.EXECUTE,),
        interfaces=(Interface.API,),
    )

    assert scope.platforms == ("platform-1",)
    assert scope.operations == (Operation.EXECUTE,)
    assert scope.interfaces == (Interface.API,)


def test_constraint_scope_is_frozen() -> None:
    scope = ConstraintScope(platforms=("platform-1",))

    with pytest.raises(ValidationError):
        scope.platforms = ("platform-2",)  # type: ignore[misc]


def test_platform_scope_rejects_out_of_scope_platform() -> None:
    scope = ConstraintScope(platforms=("platform-allowed",))
    _assert_rejected(platform="platform-disallowed", scope=scope)


def test_operation_scope_rejects_out_of_scope_operation() -> None:
    scope = ConstraintScope(operations=(Operation.READ,))
    _assert_rejected(operation=Operation.EXECUTE, scope=scope)


def test_interface_scope_rejects_out_of_scope_interface() -> None:
    scope = ConstraintScope(interfaces=(Interface.BROWSER,))
    _assert_rejected(interface=Interface.API, scope=scope)


def test_empty_scope_dimensions_are_unrestricted() -> None:
    scope = ConstraintScope()
    capability = _capability(
        platform="any-platform",
        operation=Operation.CREATE,
        interface=Interface.MCP,
        scope=scope,
    )

    assert capability.platform == "any-platform"
    assert capability.operation is Operation.CREATE
    assert capability.interface is Interface.MCP


def test_prohibited_policy_cannot_back_active_capability() -> None:
    prohibited_policy = _policy(verdict=PolicyVerdict.PROHIBITED, status=PolicyStatus.REVOKED)
    _assert_rejected(policy=prohibited_policy, active=True)


def test_high_explicit_risk_requires_approval() -> None:
    high_risk = _risk(level=RiskLevel.HIGH, mode=RiskMode.EXPLICIT)
    _assert_rejected(risk=high_risk, requires_approval=False)


def test_critical_explicit_risk_requires_approval() -> None:
    critical_risk = _risk(level=RiskLevel.CRITICAL, mode=RiskMode.EXPLICIT)
    _assert_rejected(risk=critical_risk, requires_approval=False)


def test_approval_required_policy_requires_approval() -> None:
    review_policy = _policy(verdict=PolicyVerdict.REQUIRE_REVIEW)
    _assert_rejected(policy=review_policy, requires_approval=False)


def test_allow_capability_can_be_active() -> None:
    allow_policy = _policy(verdict=PolicyVerdict.ALLOW, status=PolicyStatus.ACTIVE)
    capability = _capability(policy=allow_policy, active=True)

    assert capability.active is True
    assert capability.policy.verdict is PolicyVerdict.ALLOW


def test_low_explicit_risk_without_approval_is_valid() -> None:
    low_risk = _risk(level=RiskLevel.LOW, mode=RiskMode.EXPLICIT)
    capability = _capability(risk=low_risk, requires_approval=False)

    assert capability.risk.level is RiskLevel.LOW
    assert capability.requires_approval is False


def test_medium_explicit_risk_without_approval_is_valid() -> None:
    medium_risk = _risk(level=RiskLevel.MEDIUM, mode=RiskMode.EXPLICIT)
    capability = _capability(risk=medium_risk, requires_approval=False)

    assert capability.risk.level is RiskLevel.MEDIUM
    assert capability.requires_approval is False


def test_high_explicit_risk_with_approval_is_valid() -> None:
    high_risk = _risk(level=RiskLevel.HIGH, mode=RiskMode.EXPLICIT)
    capability = _capability(risk=high_risk, requires_approval=True)

    assert capability.risk.level is RiskLevel.HIGH
    assert capability.requires_approval is True


def test_critical_explicit_risk_with_approval_is_valid() -> None:
    critical_risk = _risk(level=RiskLevel.CRITICAL, mode=RiskMode.EXPLICIT)
    capability = _capability(risk=critical_risk, requires_approval=True)

    assert capability.risk.level is RiskLevel.CRITICAL
    assert capability.requires_approval is True


def test_require_review_policy_with_approval_is_valid() -> None:
    review_policy = _policy(verdict=PolicyVerdict.REQUIRE_REVIEW)
    capability = _capability(policy=review_policy, requires_approval=True)

    assert capability.policy.verdict is PolicyVerdict.REQUIRE_REVIEW
    assert capability.requires_approval is True


def test_no_forbidden_layer_imports() -> None:
    forbidden_imports = {
        "application",
        "infrastructure",
        "interface",
        "domain.authorization",
    }
    tree = ast.parse(CAPABILITY_PATH.read_text(encoding="utf-8"))

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
