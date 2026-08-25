# Module Specification — `domain/risk.py`

**Status:** READY FOR IMPLEMENTATION

**Version:** 1.0

**Tier:** 0

---

## Owns

- `Risk`
- `RiskMode`
- `RiskLevel`
- `effective_risk_level()`

Pure risk representation and resolution only.

---

## Must NOT depend on

- `application/*`
- `infrastructure/*`
- `interface/*`
- `domain/capability.py`
- `domain/policy.py`
- `domain/authorization.py`

No I/O, database, Redis, network, or filesystem access.

---

## Authority Boundary

### MAY

- Represent risk levels and modes.
- Validate structural consistency.
- Resolve effective risk from supplied `Risk` objects.
- Detect cycles and fail loudly.
- Resolve unknown references conservatively.

### MUST NOT

- Retrieve related risks itself.
- Query registries or repositories.
- Perform authorization.
- Decide approval requirements.
- Persist state.
- Modify policies.

---

## Contract

### `RiskLevel`

Risk levels:

    LOW
    MEDIUM
    HIGH
    CRITICAL

Risk levels are ordered from lowest to highest severity:

    LOW < MEDIUM < HIGH < CRITICAL

### `RiskMode`

Risk modes:

    EXPLICIT
    INHERITED
    AGGREGATE

`EXPLICIT` means the risk level is declared directly on the current risk.

`INHERITED` means the effective risk is resolved from a referenced source risk.

`AGGREGATE` means the effective risk is resolved from the referenced child risks and is the maximum risk among them.

### `Risk`

`Risk` is the immutable domain representation of a risk declaration.

It contains the information required to represent:

- its identity,
- its declared risk level,
- its resolution mode,
- and any related risk references required by that mode.

Cross-risk references are IDs rather than object references.

The domain object must not retrieve referenced risks itself. Resolution receives the related risks explicitly as input.

---

## `effective_risk_level()`

Signature:

    effective_risk_level(
        risk: Risk,
        related_risks: dict[str, Risk],
    ) -> RiskLevel

The function resolves the effective risk level using only the supplied `risk` and `related_risks`.

### Resolution rules

#### `EXPLICIT`

An `EXPLICIT` risk returns its own declared `RiskLevel`.

    EXPLICIT → declared level

No related risk lookup is required.

#### `INHERITED`

An `INHERITED` risk resolves the effective level of its referenced source risk recursively.

    INHERITED → source risk → effective risk level

The referenced risk must be resolved from the supplied `related_risks` mapping.

The function must never retrieve the source risk from another system.

#### `AGGREGATE`

An `AGGREGATE` risk resolves the effective level of its referenced child risks and returns the maximum effective risk.

    AGGREGATE → child risks → maximum effective level

Risk ordering is:

    LOW < MEDIUM < HIGH < CRITICAL

Therefore an aggregate containing `LOW`, `HIGH`, and `MEDIUM` resolves to `HIGH`.

---

## Unknown References

Unknown risk references must resolve conservatively.

If an `INHERITED` or `AGGREGATE` risk references a risk ID that is absent from `related_risks`, the effective risk is:

    CRITICAL

Unknown data must never silently reduce the effective risk.

The resolver must not attempt to fetch the missing risk.

---

## Cycle Detection

Risk resolution must detect cycles explicitly.

Example:

    risk-a → risk-b → risk-c → risk-a

A cycle must fail loudly through an explicit exception.

A detected cycle must **not** be converted into `CRITICAL` as an ordinary unknown-reference case.

Cycle detection must use a visited-set or equivalent deterministic mechanism.

The resolver must terminate without infinite recursion.

---

## Structural Validation

The `Risk` contract must validate structural consistency between its mode and its references.

The exact structural requirements are:

- `EXPLICIT` represents a directly declared risk.
- `INHERITED` requires the reference needed to identify its source risk.
- `AGGREGATE` requires the references needed to identify its child risks.
- References are IDs, not nested `Risk` objects.
- Risk objects are immutable/frozen contracts.

Structural validation must not retrieve or inspect external state.

---

## Domain/Application Boundary

The domain layer owns:

- risk representation,
- structural validation,
- risk ordering,
- deterministic effective-risk resolution,
- unknown-reference handling,
- cycle detection.

The application layer owns:

- retrieving risks,
- deciding which risks are relevant,
- supplying `related_risks`,
- deciding when risk resolution occurs,
- integrating risk with policy,
- integrating risk with authorization,
- deciding approval requirements,
- and execution behavior.

`domain/risk.py` must remain deterministic and side-effect free.

---

## Invariants

1. Risk levels are limited to `LOW`, `MEDIUM`, `HIGH`, and `CRITICAL`.
2. Risk modes are limited to `EXPLICIT`, `INHERITED`, and `AGGREGATE`.
3. `EXPLICIT` risk resolves to its declared level.
4. `INHERITED` risk resolves recursively through its referenced source risk.
5. `AGGREGATE` risk resolves to the maximum effective level of its child risks.
6. Risk references are resolved only from the supplied `related_risks` mapping.
7. Unknown references resolve conservatively to `CRITICAL`.
8. Cycles are detected and fail explicitly.
9. A cycle is not treated as an ordinary unknown reference.
10. Risk resolution never performs I/O or retrieves external state.
11. Risk resolution never performs authorization.
12. Risk resolution never decides approval requirements.
13. Risk resolution never modifies policies or supplied risk state.
14. The resolver is deterministic for the same supplied risk graph.

---

## Required Tests

### Risk vocabulary

    test_risk_level_has_expected_values()
    test_risk_mode_has_expected_values()

`RiskLevel` must contain exactly:

    LOW
    MEDIUM
    HIGH
    CRITICAL

`RiskMode` must contain exactly:

    EXPLICIT
    INHERITED
    AGGREGATE

### Structural validation

    test_explicit_risk_is_structurally_valid()
    test_inherited_risk_requires_source_reference()
    test_aggregate_risk_requires_child_references()

### Effective risk resolution

    test_explicit_risk_returns_declared_level()
    test_inherited_risk_resolves_source_recursively()
    test_aggregate_risk_returns_maximum_child_risk()
    test_nested_inheritance_resolves_correctly()
    test_nested_aggregate_resolves_correctly()
    test_unknown_inherited_reference_resolves_to_critical()
    test_unknown_aggregate_reference_resolves_to_critical()
    test_risk_cycle_fails_loudly()

### Dependency boundary

    test_no_forbidden_layer_imports()

The static import test must reject imports from:

    application
    infrastructure
    interface
    domain.capability
    domain.policy
    domain.authorization

It must also reject relative imports.

The test must inspect the source with `ast`, rather than relying only on runtime import behavior.

---

## Testing Constraint

Tests must verify the behavior explicitly required by this specification.

Codex must not invent speculative requirements or additional behavior.

If implementation reveals an ambiguity or missing requirement, stop and return the issue for specification review rather than silently expanding scope.

---

## Documentation

Create:

`domain/risk_struct.md`

The documentation must describe:

- what the module owns,
- allowed dependencies,
- input → processing → output,
- public contracts,
- structural invariants,
- domain/application boundary,
- effective-risk resolution,
- unknown-reference behavior,
- and cycle detection.

---

## Public Interface

The module exposes:

    Risk
    RiskMode
    RiskLevel
    effective_risk_level()

Cross-contract references must remain ID-based.

The resolver receives the related risk graph explicitly:

    effective_risk_level(
        risk,
        related_risks,
    )

It must not maintain a global risk registry.

---

## Implementation Constraints

- Use Pydantic for the `Risk` contract.
- Use `Enum` for fixed vocabularies.
- Use immutable/frozen contract semantics.
- Use IDs for cross-risk references.
- No I/O.
- No filesystem access.
- No network access.
- No database access.
- No Redis access.
- No registry/repository access.
- No imports from application, infrastructure, or interface.
- No imports from `domain/capability.py`, `domain/policy.py`, or `domain/authorization.py`.
- No global mutable state.
- No metaprogramming.
- No authorization logic.
- No approval-decision logic.
- No policy mutation.
- Explicit behavior over clever abstractions.

---

## Files Permitted

Codex may create or modify only:

    D:\academic\Zenith\domain\risk.py
    D:\academic\Zenith\domain\risk_struct.md
    D:\academic\Zenith\tests\unit\domain\test_risk.py

Nothing else.

If anything in this specification is ambiguous, stop and ask rather than guessing.