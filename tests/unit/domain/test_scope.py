import ast
from pathlib import Path

import pytest
from pydantic import ValidationError

from domain.scope import DomainScope


SCOPE_PATH = Path(__file__).parents[3] / "domain" / "scope.py"


def test_domain_scope_is_structurally_valid() -> None:
    scope = DomainScope(
        allowed_entity_types=("user", "device"),
        allowed_domains=("finance", "inventory"),
        boundaries=("boundary-1", "boundary-2"),
    )

    assert scope.allowed_entity_types == ("user", "device")
    assert scope.allowed_domains == ("finance", "inventory")
    assert scope.boundaries == ("boundary-1", "boundary-2")


def test_domain_scope_is_frozen() -> None:
    scope = DomainScope(
        allowed_entity_types=("user",),
        allowed_domains=("finance",),
        boundaries=("boundary-1",),
    )

    with pytest.raises(ValidationError):
        scope.allowed_entity_types = ("device",)  # type: ignore[misc]

    with pytest.raises(ValidationError):
        scope.allowed_domains = ("ops",)  # type: ignore[misc]

    with pytest.raises(ValidationError):
        scope.boundaries = ("boundary-2",)  # type: ignore[misc]


def test_domain_scope_defaults_to_empty_dimensions() -> None:
    scope = DomainScope()

    assert scope.allowed_entity_types == ()
    assert scope.allowed_domains == ()
    assert scope.boundaries == ()


def test_domain_scope_accepts_entity_types() -> None:
    scope = DomainScope(allowed_entity_types=("user", "document", "service"))

    assert scope.allowed_entity_types == ("user", "document", "service")
    assert scope.allowed_domains == ()
    assert scope.boundaries == ()


def test_domain_scope_accepts_domains() -> None:
    scope = DomainScope(allowed_domains=("security", "identity"))

    assert scope.allowed_domains == ("security", "identity")
    assert scope.allowed_entity_types == ()
    assert scope.boundaries == ()


def test_domain_scope_accepts_boundaries() -> None:
    scope = DomainScope(boundaries=("tenant-1", "region-us-east"))

    assert scope.boundaries == ("tenant-1", "region-us-east")
    assert scope.allowed_entity_types == ()
    assert scope.allowed_domains == ()


def test_domain_scope_uses_immutable_tuples() -> None:
    scope = DomainScope(
        allowed_entity_types=["user"],  # type: ignore[arg-type]
        allowed_domains=["finance"],  # type: ignore[arg-type]
        boundaries=["boundary-1"],  # type: ignore[arg-type]
    )

    assert isinstance(scope.allowed_entity_types, tuple)
    assert isinstance(scope.allowed_domains, tuple)
    assert isinstance(scope.boundaries, tuple)
    assert scope.allowed_entity_types == ("user",)
    assert scope.allowed_domains == ("finance",)
    assert scope.boundaries == ("boundary-1",)


def test_empty_scope_dimensions_do_not_require_external_state() -> None:
    scope = DomainScope()
    assert isinstance(scope, DomainScope)
    assert len(scope.allowed_entity_types) == 0
    assert len(scope.allowed_domains) == 0
    assert len(scope.boundaries) == 0


def test_no_forbidden_layer_imports() -> None:
    forbidden_imports = {
        "application",
        "infrastructure",
        "interface",
        "domain.worldstate",
    }
    tree = ast.parse(SCOPE_PATH.read_text(encoding="utf-8"))

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
    tree = ast.parse(SCOPE_PATH.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            assert node.level == 0, f"Relative import detected: level={node.level}, module={node.module}"
