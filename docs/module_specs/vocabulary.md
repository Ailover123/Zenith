# Module Specification — domain/vocabulary.py

# Status

READY FOR IMPLEMENTATION

# Version

1.0

# Tier

0

---

# Owns

This module owns the foundational domain vocabulary used throughout the Zenith system.

It owns exactly:

- Operation
- Interface

These are pure enumerations.

This module provides vocabulary only.

It does not own domain models, validation, authorization, policy evaluation, risk resolution, capability logic, execution logic, or runtime behavior.

---

# Must NOT depend on

This module must not depend on any Zenith module.

Forbidden Zenith dependencies include:

- domain.*
- application.*
- infrastructure.*
- interface.*

It must not import:

- Pydantic
- Any third-party package
- Any project-local module
- Any runtime service

The only permitted import is:

- enum.Enum from the Python standard library

No relative imports are permitted.

---

# Authority Boundary

The vocabulary module owns pure declarations only.

It MAY:

- Define Operation.
- Define Interface.
- Provide fixed enum membership.
- Provide enum values required by the domain contract.

It MUST NOT:

- Perform validation beyond normal Enum behavior.
- Contain custom validators.
- Contain helper methods.
- Contain business logic.
- Perform authorization.
- Perform policy evaluation.
- Perform risk evaluation.
- Perform capability evaluation.
- Perform I/O.
- Access databases.
- Access Redis.
- Access files.
- Access networks.
- Access registries.
- Access repositories.
- Import other Zenith modules.
- Maintain global mutable state.

The module must remain deterministic and dependency-free.

---

# Operation

Operation represents the foundational category of action that a capability or domain contract may describe.

The enum must contain exactly:

- READ
- CREATE
- MODIFY
- EXECUTE
- DELEGATE

No additional Operation values may be introduced without a specification change.

# Operation meanings

## READ

Represents obtaining or observing information.

## CREATE

Represents creating a new resource, object, or state.

## MODIFY

Represents changing existing state or data.

## EXECUTE

Represents performing an action or invoking an executable capability.

## DELEGATE

Represents transferring or granting authority within the authorization model.

These meanings are descriptive only.

Operation does not implement behavior associated with any operation.

---

# Interface

Interface represents the interaction boundary through which a capability or operation may be exposed.

The enum must contain exactly:

- API
- MCP
- BROWSER
- DEVICE
- A2A

No additional Interface values may be introduced without a specification change.

# Interface meanings

## API

Represents interaction through an API boundary.

## MCP

Represents interaction through an MCP boundary.

## BROWSER

Represents interaction through a browser-based interface.

## DEVICE

Represents interaction with a device interface.

## A2A

Represents agent-to-agent interaction.

These meanings are descriptive only.

Interface does not implement communication, networking, execution, or integration behavior.

---

# Enum Semantics

Operation and Interface must use Python Enum semantics.

They must be ordinary enums derived from:

- enum.Enum

No Pydantic models are required.

No custom base classes are required.

No custom methods are required.

No validators are required.

No properties are required.

No helper functions are required.

The enums must remain simple declarations.

---

# Exact Membership Invariant

Operation must contain exactly:

- READ
- CREATE
- MODIFY
- EXECUTE
- DELEGATE

Interface must contain exactly:

- API
- MCP
- BROWSER
- DEVICE
- A2A

The implementation must not silently add aliases or additional members.

Enum membership is part of the domain contract.

---

# Value Representation

The enum names and values must be stable domain vocabulary.

The implementation must use explicit string values.

Expected Operation values:

- READ = "read"
- CREATE = "create"
- MODIFY = "modify"
- EXECUTE = "execute"
- DELEGATE = "delegate"

Expected Interface values:

- API = "api"
- MCP = "mcp"
- BROWSER = "browser"
- DEVICE = "device"
- A2A = "a2a"

No alternative spellings or implicit numeric enum values are permitted.

---

# Domain Boundary

Vocabulary is the lowest-level domain declaration layer.

Other domain modules may depend on vocabulary.

Examples include:

- domain.policy
- domain.capability

However, vocabulary must never depend on those modules.

The dependency direction is therefore:

vocabulary
    ↓
other domain contracts

and never:

vocabulary
    ↓
policy
    ↓
capability
    ↓
authorization

Vocabulary remains foundational.

---

# Input → Processing → Output

This module does not perform processing.

Its conceptual flow is:

Operation declaration
    ↓
fixed enum member

Interface declaration
    ↓
fixed enum member

There is no external input.

There is no runtime resolution.

There is no persistence.

There is no side effect.

The output of this module is the two immutable enum types:

- Operation
- Interface

---

# Structural Invariants

1. Operation exists.
2. Interface exists.
3. Operation contains exactly five members.
4. Interface contains exactly five members.
5. Operation members are READ, CREATE, MODIFY, EXECUTE, and DELEGATE.
6. Interface members are API, MCP, BROWSER, DEVICE, and A2A.
7. Operation values are read, create, modify, execute, and delegate.
8. Interface values are api, mcp, browser, device, and a2a.
9. Only enum.Enum from the Python standard library may be imported.
10. No Zenith module may be imported.
11. No third-party dependency may be imported.
12. No relative imports may be used.
13. No validators may exist.
14. No helper functions may exist.
15. No business logic may exist.
16. No I/O may occur.
17. No global mutable state may exist.
18. Vocabulary must remain independent of every other Zenith module.

---

# Dependency Boundary

The module must have no project dependencies.

Allowed:

- Python standard library enum.Enum

Forbidden:

- domain.vocabulary imports from itself or other domain modules
- domain.policy
- domain.risk
- domain.capability
- domain.authorization
- application.*
- infrastructure.*
- interface.*
- Pydantic
- Any third-party package

The implementation should therefore be trivially inspectable with AST-based dependency tests.

---

# Required Tests

The test suite must verify the exact vocabulary and dependency boundary.

## Operation vocabulary

Test:

- test_operation_has_expected_values

The test must verify:

- Exact member names.
- Exact member values.
- No additional members.

Expected:

- READ = "read"
- CREATE = "create"
- MODIFY = "modify"
- EXECUTE = "execute"
- DELEGATE = "delegate"

## Interface vocabulary

Test:

- test_interface_has_expected_values

The test must verify:

- Exact member names.
- Exact member values.
- No additional members.

Expected:

- API = "api"
- MCP = "mcp"
- BROWSER = "browser"
- DEVICE = "device"
- A2A = "a2a"

## Zenith dependency boundary

Test:

- test_no_zenith_module_imports

The test must inspect vocabulary.py using AST.

It must reject imports from any Zenith package or module.

No runtime-import-only check is sufficient.

## Third-party dependency boundary

Test:

- test_no_third_party_imports

The test must inspect the source using AST.

Only enum.Enum from the Python standard library is permitted.

Imports such as Pydantic or any other third-party package must fail the test.

---

# Testing Constraint

Tests must verify only the behavior explicitly required by this specification.

Do not add tests for:

- authorization
- policy behavior
- risk behavior
- capability behavior
- serialization frameworks
- database behavior
- runtime registration
- execution behavior
- network behavior
- external integrations

Vocabulary must remain intentionally simple.

If implementation reveals an ambiguity in the enum names or values, stop and return the issue for specification review rather than guessing.

---

# Documentation

Create:

domain/vocabulary_struct.md

The documentation must describe:

- Module ownership.
- Operation vocabulary.
- Interface vocabulary.
- Exact enum membership.
- Exact enum values.
- Allowed dependency boundary.
- Forbidden dependencies.
- Input → processing → output.
- Foundational role of vocabulary.
- Domain dependency direction.
- Structural invariants.
- Testing requirements.

The documentation must make clear that vocabulary contains declarations only and no business logic.

---

# Public Interface

The module exposes exactly:

- Operation
- Interface

Nothing else is part of the public domain contract.

Do not expose helper functions.

Do not expose validators.

Do not expose utility classes.

Do not expose runtime services.

Do not expose project-specific dependencies.

---

# Implementation Constraints

- Use enum.Enum.
- Use explicit string values.
- Keep the implementation minimal.
- No Pydantic.
- No third-party libraries.
- No Zenith imports.
- No application imports.
- No infrastructure imports.
- No interface imports.
- No relative imports.
- No validators.
- No helper methods.
- No helper functions.
- No business logic.
- No I/O.
- No filesystem access.
- No network access.
- No database access.
- No Redis access.
- No registry access.
- No repository access.
- No global mutable state.
- No metaprogramming.
- Explicit declarations over abstractions.

---

# Files Permitted

The implementation may create or modify only:

D:\academic\Zenith\domain\vocabulary.py

D:\academic\Zenith\domain\vocabulary_struct.md

D:\academic\Zenith\tests\unit\domain\test_vocabulary.py

Nothing else.

If anything in this specification is ambiguous, stop and ask rather than guessing.