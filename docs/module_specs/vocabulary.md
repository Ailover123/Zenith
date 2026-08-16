# Module Specification — `domain/vocabulary.py`

## Owns

- `Operation`
- `Interface`

## Must NOT depend on

- Any Zenith module
- Pydantic
- Application, infrastructure, or interface layers

Only `enum.Enum` from Python standard library.

## Authority Boundary

Pure declarations only. No logic, validators, I/O, or helper methods.

## Contract

### Operation

READ, CREATE, MODIFY, EXECUTE, DELEGATE

### Interface

API, MCP, BROWSER, DEVICE, A2A

## Invariants

- Exact enum membership as defined above.
- No Zenith imports.
- No third-party imports.

## Required Tests

```text
test_operation_has_expected_values()
test_interface_has_expected_values()
test_no_zenith_module_imports()
test_no_third_party_imports()