# domain/vocabulary.py

## Ownership

This module owns the shared domain vocabularies for operation types and interface types:

- `Operation`
- `Interface`

## Infrastructure Dependencies

None. The module has no infrastructure, application, interface, third-party, or Pydantic dependencies.

## Input/Output

Inputs are enum member names used by other layers. Outputs are stable string enum values.

## Public Contracts

- `Operation` v1: `READ`, `CREATE`, `MODIFY`, `EXECUTE`, `DELEGATE`
- `Interface` v1: `API`, `MCP`, `BROWSER`, `DEVICE`, `A2A`

## Relevant Invariants

- Members and values must exactly match the v1 vocabulary contracts.
- The module must not contain validators, helper functions, or unrelated classes.
- The only allowed import is `from enum import Enum`.

## Dependency Boundary

`domain/vocabulary.py` is a pure domain module. It must not import Zenith modules or third-party packages.
