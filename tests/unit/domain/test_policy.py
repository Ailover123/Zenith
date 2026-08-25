import ast
from pathlib import Path

from domain.policy import Policy, PolicyStatus, PolicyVerdict
from domain.vocabulary import Interface, Operation


POLICY_PATH = Path(__file__).parents[3] / "domain" / "policy.py"


def _policy(
    *,
    verdict: PolicyVerdict = PolicyVerdict.ALLOW,
    status: PolicyStatus = PolicyStatus.DISCOVERED,
    reviewed_by_human: bool = False,
) -> Policy:
    return Policy(
        id="policy-1",
        platform="platform",
        operation=Operation.EXECUTE,
        interface=Interface.API,
        verdict=verdict,
        status=status,
        version=1,
        reviewed_by_human=reviewed_by_human,
    )


def _assert_rejected(**kwargs: object) -> None:
    try:
        _policy(**kwargs)
    except ValueError:
        return

    raise AssertionError("policy state was accepted")


def test_prohibited_policy_cannot_be_active() -> None:
    """PROHIBITED + ACTIVE is rejected."""
    _assert_rejected(
        verdict=PolicyVerdict.PROHIBITED,
        status=PolicyStatus.ACTIVE,
        reviewed_by_human=True,
    )


def test_active_policy_requires_human_review() -> None:
    """ACTIVE + reviewed_by_human=False is rejected."""
    _assert_rejected(status=PolicyStatus.ACTIVE, reviewed_by_human=False)


def test_approved_policy_requires_human_review() -> None:
    """APPROVED + reviewed_by_human=False is rejected."""
    _assert_rejected(status=PolicyStatus.APPROVED, reviewed_by_human=False)


def test_reviewed_active_policy_is_valid() -> None:
    """ACTIVE + reviewed_by_human=True is accepted."""
    policy = _policy(status=PolicyStatus.ACTIVE, reviewed_by_human=True)

    assert policy.status is PolicyStatus.ACTIVE
    assert policy.reviewed_by_human is True


def test_allow_active_policy_is_valid() -> None:
    """ALLOW + ACTIVE + reviewed_by_human=True is accepted."""
    policy = _policy(
        verdict=PolicyVerdict.ALLOW,
        status=PolicyStatus.ACTIVE,
        reviewed_by_human=True,
    )

    assert policy.verdict is PolicyVerdict.ALLOW
    assert policy.status is PolicyStatus.ACTIVE


def test_approval_required_active_policy_is_valid() -> None:
    """REQUIRE_REVIEW + ACTIVE + reviewed_by_human=True is structurally valid."""
    policy = _policy(
        verdict=PolicyVerdict.REQUIRE_REVIEW,
        status=PolicyStatus.ACTIVE,
        reviewed_by_human=True,
    )

    assert policy.verdict is PolicyVerdict.REQUIRE_REVIEW
    assert policy.status is PolicyStatus.ACTIVE


def test_no_forbidden_layer_imports() -> None:
    """Policy must not import application, infrastructure, or interface modules."""
    forbidden_roots = {"application", "infrastructure", "interface"}
    tree = ast.parse(POLICY_PATH.read_text(encoding="utf-8"))

    for import_node in ast.walk(tree):
        if isinstance(import_node, ast.Import):
            imported_roots = {
                alias.name.split(".", maxsplit=1)[0]
                for alias in import_node.names
            }
        elif isinstance(import_node, ast.ImportFrom):
            assert import_node.level == 0, "relative imports are not permitted"
            imported_roots = {
                import_node.module.split(".", maxsplit=1)[0]
                if import_node.module is not None
                else ""
            }
        else:
            continue

        assert imported_roots.isdisjoint(forbidden_roots)
