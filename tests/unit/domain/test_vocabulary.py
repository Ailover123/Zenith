import ast
from pathlib import Path

from domain.vocabulary import Interface, Operation


VOCABULARY_PATH = Path(__file__).parents[3] / "domain" / "vocabulary.py"


def _imports() -> list[ast.Import | ast.ImportFrom]:
    tree = ast.parse(VOCABULARY_PATH.read_text(encoding="utf-8"))
    return [
        node
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
    ]


def test_operation_has_expected_values() -> None:
    assert [(item.name, item.value) for item in Operation] == [
        ("READ", "read"),
        ("CREATE", "create"),
        ("MODIFY", "modify"),
        ("EXECUTE", "execute"),
        ("DELEGATE", "delegate"),
    ]


def test_interface_has_expected_values() -> None:
    assert [(item.name, item.value) for item in Interface] == [
        ("API", "api"),
        ("MCP", "mcp"),
        ("BROWSER", "browser"),
        ("DEVICE", "device"),
        ("A2A", "a2a"),
    ]


def test_no_zenith_module_imports() -> None:
    zenith_roots = {"application", "domain", "infrastructure", "interface"}

    for import_node in _imports():
        if isinstance(import_node, ast.Import):
            imported_roots = {alias.name.split(".", maxsplit=1)[0] for alias in import_node.names}
        else:
            assert import_node.level == 0, "relative imports are not permitted"
            imported_roots = {
                import_node.module.split(".", maxsplit=1)[0]
                if import_node.module is not None
                else ""
            }

        assert imported_roots.isdisjoint(zenith_roots)


def test_no_third_party_imports() -> None:
    imports = _imports()

    assert len(imports) == 1
    assert isinstance(imports[0], ast.ImportFrom)
    assert imports[0].module == "enum"
    assert imports[0].level == 0
    assert [alias.name for alias in imports[0].names] == ["Enum"]
