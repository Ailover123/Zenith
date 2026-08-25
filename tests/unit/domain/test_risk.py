import ast
from pathlib import Path

from domain.risk import Risk, RiskLevel, RiskMode, effective_risk_level


RISK_PATH = Path(__file__).parents[3] / "domain" / "risk.py"


def _risk(
    *,
    id: str = "risk-1",
    level: RiskLevel = RiskLevel.LOW,
    mode: RiskMode = RiskMode.EXPLICIT,
    source_risk_id: str | None = None,
    child_risk_ids: tuple[str, ...] = (),
) -> Risk:
    return Risk(
        id=id,
        level=level,
        mode=mode,
        source_risk_id=source_risk_id,
        child_risk_ids=child_risk_ids,
    )


def _assert_rejected(**kwargs: object) -> None:
    try:
        _risk(**kwargs)
    except ValueError:
        return

    raise AssertionError("risk state was accepted")


def test_risk_level_has_expected_values() -> None:
    assert [(item.name, item.value) for item in RiskLevel] == [
        ("LOW", "low"),
        ("MEDIUM", "medium"),
        ("HIGH", "high"),
        ("CRITICAL", "critical"),
    ]


def test_risk_mode_has_expected_values() -> None:
    assert [(item.name, item.value) for item in RiskMode] == [
        ("EXPLICIT", "explicit"),
        ("INHERITED", "inherited"),
        ("AGGREGATE", "aggregate"),
    ]


def test_explicit_risk_is_structurally_valid() -> None:
    risk = _risk(level=RiskLevel.MEDIUM, mode=RiskMode.EXPLICIT)

    assert risk.level is RiskLevel.MEDIUM
    assert risk.mode is RiskMode.EXPLICIT


def test_inherited_risk_requires_source_reference() -> None:
    _assert_rejected(mode=RiskMode.INHERITED)


def test_aggregate_risk_requires_child_references() -> None:
    _assert_rejected(mode=RiskMode.AGGREGATE)


def test_explicit_risk_returns_declared_level() -> None:
    risk = _risk(level=RiskLevel.HIGH)

    assert effective_risk_level(risk, {}) is RiskLevel.HIGH


def test_inherited_risk_resolves_source_recursively() -> None:
    inherited = _risk(id="inherited", mode=RiskMode.INHERITED, source_risk_id="source")
    source = _risk(id="source", level=RiskLevel.HIGH)

    assert effective_risk_level(inherited, {"source": source}) is RiskLevel.HIGH


def test_aggregate_risk_returns_maximum_child_risk() -> None:
    aggregate = _risk(
        id="aggregate",
        mode=RiskMode.AGGREGATE,
        child_risk_ids=("low", "high", "medium"),
    )
    related_risks = {
        "low": _risk(id="low", level=RiskLevel.LOW),
        "high": _risk(id="high", level=RiskLevel.HIGH),
        "medium": _risk(id="medium", level=RiskLevel.MEDIUM),
    }

    assert effective_risk_level(aggregate, related_risks) is RiskLevel.HIGH


def test_nested_inheritance_resolves_correctly() -> None:
    first = _risk(id="first", mode=RiskMode.INHERITED, source_risk_id="second")
    second = _risk(id="second", mode=RiskMode.INHERITED, source_risk_id="third")
    third = _risk(id="third", level=RiskLevel.MEDIUM)

    assert effective_risk_level(first, {"second": second, "third": third}) is RiskLevel.MEDIUM


def test_nested_aggregate_resolves_correctly() -> None:
    aggregate = _risk(
        id="aggregate",
        mode=RiskMode.AGGREGATE,
        child_risk_ids=("nested", "medium"),
    )
    nested = _risk(
        id="nested",
        mode=RiskMode.AGGREGATE,
        child_risk_ids=("low", "high"),
    )
    related_risks = {
        "nested": nested,
        "low": _risk(id="low", level=RiskLevel.LOW),
        "high": _risk(id="high", level=RiskLevel.HIGH),
        "medium": _risk(id="medium", level=RiskLevel.MEDIUM),
    }

    assert effective_risk_level(aggregate, related_risks) is RiskLevel.HIGH


def test_unknown_inherited_reference_resolves_to_critical() -> None:
    risk = _risk(id="risk", mode=RiskMode.INHERITED, source_risk_id="missing")

    assert effective_risk_level(risk, {}) is RiskLevel.CRITICAL


def test_unknown_aggregate_reference_resolves_to_critical() -> None:
    risk = _risk(id="risk", mode=RiskMode.AGGREGATE, child_risk_ids=("missing",))

    assert effective_risk_level(risk, {}) is RiskLevel.CRITICAL


def test_risk_cycle_fails_loudly() -> None:
    first = _risk(id="first", mode=RiskMode.INHERITED, source_risk_id="second")
    second = _risk(id="second", mode=RiskMode.INHERITED, source_risk_id="first")

    try:
        effective_risk_level(first, {"first": first, "second": second})
    except ValueError:
        return

    raise AssertionError("risk cycle was not rejected")


def test_no_forbidden_layer_imports() -> None:
    forbidden_imports = {
        "application",
        "infrastructure",
        "interface",
        "domain.capability",
        "domain.policy",
        "domain.authorization",
    }
    tree = ast.parse(RISK_PATH.read_text(encoding="utf-8"))

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
