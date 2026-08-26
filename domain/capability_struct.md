# domain/capability.py

## Module Ownership

This module owns the pure domain representation of a capability and the structural constraints required for that capability to be considered valid:

- `CapabilityTemplate`
- `ConstraintScope`
- `Capability`

It does not own runtime authorization, execution, registration, or external resolution.

## Allowed Dependencies

Allowed dependencies are limited to:

- Python standard library type support
- Pydantic for composite contracts and frozen/immutable model semantics
- Shared vocabulary from `domain.vocabulary` (`Operation`, `Interface`)
- `Policy` and `PolicyVerdict` from `domain.policy`
- `Risk`, `RiskLevel`, and `RiskMode` from `domain.risk`

## Forbidden Dependencies

This module must not import:

- `application/*`
- `infrastructure/*`
- `interface/*`
- `domain.authorization`
- Runtime services, registries, repositories, persistence systems, databases, Redis, external APIs, network clients, or filesystem interfaces.

No relative imports are permitted.

## Input -> Processing -> Output

```text
CapabilityTemplate
        +
ConstraintScope
        +
Policy
        +
Risk
        +
Capability declaration
        ↓
structural validation
        ↓
valid immutable Capability
```

- Invalid combinations fail during construction with an explicit validation error (`ValueError`).
- No external state is read or modified.
- No authorization decision is produced.

## Public Contracts

### `CapabilityTemplate`

`CapabilityTemplate` represents the reusable domain definition of a capability:

- `id: str`
- `name: str`
- `operation: Operation`
- `interface: Interface`

`CapabilityTemplate` is a frozen Pydantic model.

### `ConstraintScope`

`ConstraintScope` represents the structural scope within which a capability may be used:

- `platforms: tuple[str, ...]` (default: `()`)
- `operations: tuple[Operation, ...]` (default: `()`)
- `interfaces: tuple[Interface, ...]` (default: `()`)

An empty constraint collection means that dimension is not additionally restricted by the scope.

`ConstraintScope` is a frozen Pydantic model.

### `Capability`

`Capability` represents a concrete domain capability declaration:

- `id: str`
- `template_id: str`
- `platform: str`
- `operation: Operation`
- `interface: Interface`
- `policy: Policy`
- `risk: Risk`
- `scope: ConstraintScope` (default: `ConstraintScope()`)
- `requires_approval: bool`
- `active: bool`

`Capability` is a frozen Pydantic model that performs validation of structural invariants during model construction.

## Structural Invariants

1. `CapabilityTemplate` is immutable.
2. `ConstraintScope` is immutable.
3. `Capability` is immutable.
4. A `PROHIBITED` policy cannot back an active capability.
5. Explicit `HIGH` risk requires `requires_approval=True`.
6. Explicit `CRITICAL` risk requires `requires_approval=True`.
7. `REQUIRE_REVIEW` policy requires `requires_approval=True`.
8. Non-empty platform scope must contain the capability platform.
9. Non-empty operation scope must contain the capability operation.
10. Non-empty interface scope must contain the capability interface.
11. Capability validation is structural only.
12. The capability module never performs authorization.
13. The capability module never retrieves external state.
14. The capability module never modifies policies.
15. The capability module never resolves external risk state.
16. The capability module performs no I/O.
17. The capability module contains no global mutable state.
18. Cross-module dependencies remain within the declared domain boundary.

## Policy Consistency

- A capability backed by a `PROHIBITED` policy cannot be active (`policy.verdict is PolicyVerdict.PROHIBITED` and `active == True` is rejected).
- The capability module does not modify the policy to make the capability valid.

## Risk Consistency

- Only explicit risk levels are evaluated for the structural approval invariant.
- Explicit `HIGH` or `CRITICAL` risk requires `requires_approval=True`.
- Explicit `LOW` or `MEDIUM` risk does not create an approval requirement by itself.
- Inherited and aggregate risk resolution remains owned by `domain.risk`. The capability module does not resolve or query external risk graphs.

## Approval Requirements

- If `policy.verdict is PolicyVerdict.REQUIRE_REVIEW`, then `requires_approval=True` is mandatory.
- If explicit risk is `HIGH` or `CRITICAL`, then `requires_approval=True` is mandatory.
- The capability module does not execute the approval process or decide approval workflows; it only enforces structural consistency.

## Constraint-Scope Behavior

- If `scope.platforms` is non-empty, `platform` must be in `scope.platforms`.
- If `scope.operations` is non-empty, `operation` must be in `scope.operations`.
- If `scope.interfaces` is non-empty, `interface` must be in `scope.interfaces`.
- If a constraint dimension is empty, no restriction is imposed on that dimension.
- Scope validation is strictly structural.

## Domain/Application Boundary

### Domain owns:
- Capability, template, and constraint-scope representation
- Construction-time structural validation
- Policy/capability consistency
- Risk/capability consistency
- Approval-requirement consistency
- Deterministic scope validation

### Application owns:
- Retrieving capability definitions, policies, and risks
- Deciding which capability is relevant
- Registering capabilities and lifecycle management
- Approval workflow orchestration and execution

### Authorization owns:
- Evaluating actor authorization to use a capability
- Grant and delegation evaluation
- Runtime authorization enforcement

## Public Interface

The module exposes:

- `CapabilityTemplate`
- `ConstraintScope`
- `Capability`
