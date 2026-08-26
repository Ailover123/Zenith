# Module Specification — `domain/capability.py`

**Status:** READY FOR IMPLEMENTATION

**Version:** 1.0

**Tier:** 0

---

## Owns

- `CapabilityTemplate`
- `ConstraintScope`
- `Capability`

This module owns the pure domain representation of a capability and the structural constraints required for that capability to be considered valid.

It does not own runtime authorization.

---

## Must NOT depend on

- `application/*`
- `infrastructure/*`
- `interface/*`

No I/O.

Allowed domain dependencies are limited to:

- shared vocabulary from `domain.vocabulary`
- `Policy` from `domain.policy`
- `Risk` and risk contracts from `domain.risk`

The module must not import:

- `domain.authorization`
- runtime services
- registries
- repositories
- persistence systems
- external APIs
- network clients
- filesystem interfaces

---

## Authority Boundary

### MAY

- Represent capability contracts.
- Represent capability templates.
- Represent capability constraint scopes.
- Validate structural consistency.
- Validate capability/policy consistency.
- Validate capability/risk consistency.
- Ensure prohibited policies cannot be active.
- Ensure high/critical explicit risk requires approval.
- Ensure approval-required policy requires approval.
- Represent capability constraints.
- Represent the relationship between a capability and its policy/risk declarations.

### MUST NOT

- Perform runtime authorization.
- Query registries.
- Determine current registration status.
- Discover capabilities from external systems.
- Access databases.
- Access Redis.
- Access the network.
- Access the filesystem.
- Execute capabilities.
- Modify policies.
- Resolve external risk state.
- Determine whether a user is authorized.
- Create authorization decisions.
- Decide runtime approval flow.

The domain validates the supplied capability state.

The application/authorization layers determine what happens with that capability at runtime.

---

## Contract Version

```text
CapabilityTemplate v1

ConstraintScope v1

Capability v1
```

---

## Contract

### `CapabilityTemplate`

`CapabilityTemplate` represents the reusable domain definition of a capability.

It describes what operation/interface combination a capability represents without performing execution or authorization.

The template is immutable.

The contract contains:

```text
id: str
name: str
operation: Operation
interface: Interface
```

### `ConstraintScope`

`ConstraintScope` represents the structural scope within which a capability may be used.

It contains ID/value based constraints only and must not contain runtime services or external objects.

The contract contains:

```text
platforms: tuple[str, ...]
operations: tuple[Operation, ...]
interfaces: tuple[Interface, ...]
```

An empty constraint collection means that dimension is not additionally restricted by the scope.

`ConstraintScope` is immutable.

### `Capability`

`Capability` represents a concrete domain capability declaration.

It associates:

- a capability identity,
- a capability template,
- a platform,
- an operation,
- an interface,
- a policy,
- a risk declaration,
- a constraint scope,
- and whether approval is required.

Cross-contract relationships must use domain contracts or IDs as explicitly defined by the contract. The capability module must not retrieve related objects itself.

The contract contains:

```text
id: str
template_id: str
platform: str
operation: Operation
interface: Interface
policy: Policy
risk: Risk
scope: ConstraintScope
requires_approval: bool
active: bool
```

`Capability` is immutable.

---

## Structural Validation

The domain validates the supplied capability state during construction.

### Template consistency

A `Capability` must preserve the operation and interface represented by its template.

Therefore:

```text
capability.operation == template.operation
capability.interface == template.interface
```

must hold whenever the template information is supplied as part of the capability contract.

The capability module must not retrieve templates from registries to perform this validation.

---

## Policy Consistency

The capability must respect the supplied `Policy`.

### Prohibited policy

A capability backed by a `PROHIBITED` policy cannot be active.

```text
PROHIBITED policy + active capability
    → invalid
```

Construction must fail explicitly.

The capability module must not modify the policy to make the capability valid.

---

## Risk Consistency

The capability must respect the supplied risk declaration.

Only explicit risk level is used for the structural approval invariant.

### High risk

If the capability has:

```text
RiskMode.EXPLICIT
```

and:

```text
RiskLevel.HIGH
```

then:

```text
requires_approval == True
```

is mandatory.

### Critical risk

If the capability has:

```text
RiskMode.EXPLICIT
```

and:

```text
RiskLevel.CRITICAL
```

then:

```text
requires_approval == True
```

is mandatory.

Therefore:

```text
HIGH + EXPLICIT + requires_approval=False
    → invalid

CRITICAL + EXPLICIT + requires_approval=False
    → invalid
```

Lower explicit risk does not create an approval requirement by itself.

Inherited and aggregate risk resolution is owned by `domain.risk`.

This module must not retrieve or resolve external risk state.

---

## Approval-Required Policy

If the supplied policy has a verdict requiring approval:

```text
PolicyVerdict.REQUIRE_REVIEW
```

then:

```text
requires_approval == True
```

is mandatory.

Therefore:

```text
REQUIRE_REVIEW + requires_approval=False
    → invalid
```

The capability module does not perform the approval process.

It only validates that the capability declaration is structurally consistent with the policy.

---

## Constraint Scope

`ConstraintScope` provides structural restrictions for a capability.

### Platform constraints

If `platforms` is non-empty, the capability platform must belong to the declared platform scope.

```text
platforms != empty
and capability.platform not in platforms
    → invalid
```

If `platforms` is empty, no platform restriction is imposed by the scope.

### Operation constraints

If `operations` is non-empty, the capability operation must belong to the declared operation scope.

```text
operations != empty
and capability.operation not in operations
    → invalid
```

If `operations` is empty, no operation restriction is imposed by the scope.

### Interface constraints

If `interfaces` is non-empty, the capability interface must belong to the declared interface scope.

```text
interfaces != empty
and capability.interface not in interfaces
    → invalid
```

If `interfaces` is empty, no interface restriction is imposed by the scope.

Scope validation is structural only.

The module must not query any external platform, registry, or runtime system.

---

## Input → Processing → Output

The domain flow is:

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

Invalid combinations fail during construction with an explicit validation error.

No external state is read.

No external state is modified.

No authorization decision is produced.

---

## Invariants

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

---

## Domain/Application Boundary

### Domain owns

- capability representation,
- capability template representation,
- constraint scope representation,
- structural validation,
- policy/capability consistency,
- risk/capability consistency,
- approval-requirement consistency,
- deterministic scope validation.

### Application owns

- retrieving capability definitions,
- retrieving policies,
- retrieving risks,
- deciding which capability is relevant,
- registering capabilities,
- lifecycle management,
- orchestration,
- approval workflow,
- runtime execution.

### Authorization owns

- evaluating whether an actor may use a capability,
- evaluating grants and delegations,
- producing authorization decisions,
- enforcing runtime authorization.

`domain/capability.py` must not absorb authorization responsibilities.

---

## Relationship With `domain.policy`

`domain.capability` may depend on `domain.policy`.

The capability module may inspect supplied policy fields such as:

```text
policy.verdict
policy.status
```

It may validate capability/policy consistency.

It must not:

- activate policies,
- revoke policies,
- modify policies,
- persist policies,
- discover policies,
- retrieve policies.

---

## Relationship With `domain.risk`

`domain.capability` may depend on `domain.risk`.

The capability module may inspect supplied risk declarations such as:

```text
risk.mode
risk.level
```

It may enforce the structural rule that explicit high/critical risk requires approval.

It must not:

- retrieve related risks,
- resolve risk graphs,
- modify risks,
- persist risks,
- query risk registries.

Risk resolution remains owned by `domain.risk`.

---

## Dependency Direction

The dependency direction must remain:

```text
domain.vocabulary
        ↑
domain.policy
        ↑
domain.risk
        ↑
domain.capability
```

`domain.capability` must not introduce dependencies upward into:

```text
application
infrastructure
interface
```

It must also not depend on:

```text
domain.authorization
```

because authorization is a higher-level runtime concern.

---

## Required Tests

### Capability template

```text
test_capability_template_is_structurally_valid()
test_capability_template_is_frozen()
```

### Constraint scope

```text
test_constraint_scope_is_structurally_valid()
test_constraint_scope_is_frozen()
test_platform_scope_rejects_out_of_scope_platform()
test_operation_scope_rejects_out_of_scope_operation()
test_interface_scope_rejects_out_of_scope_interface()
test_empty_scope_dimensions_are_unrestricted()
```

### Capability invariants

```text
test_prohibited_policy_cannot_back_active_capability()
test_high_explicit_risk_requires_approval()
test_critical_explicit_risk_requires_approval()
test_approval_required_policy_requires_approval()
```

### Valid capability states

```text
test_allow_capability_can_be_active()
test_low_explicit_risk_without_approval_is_valid()
test_medium_explicit_risk_without_approval_is_valid()
test_high_explicit_risk_with_approval_is_valid()
test_critical_explicit_risk_with_approval_is_valid()
test_require_review_policy_with_approval_is_valid()
```

### Dependency boundary

```text
test_no_forbidden_layer_imports()
```

The static import test must reject imports from:

```text
application
infrastructure
interface
domain.authorization
```

It must also reject relative imports.

The test must inspect source using `ast`.

For `ImportFrom` nodes:

```text
assert import_node.level == 0
```

must be enforced.

Forbidden imports must be checked by module root rather than only exact string equality so that nested forbidden modules are also rejected.

---

## Testing Constraint

Tests must verify behavior explicitly required by this specification.

Tests must not invent runtime authorization behavior.

Tests must not require databases, Redis, network access, filesystem access, registries, or external services.

Tests must validate construction-time structural behavior.

If implementation reveals an ambiguity or missing requirement, stop and return the issue for specification review rather than silently expanding scope.

---

## Documentation

Create:

```text
domain/capability_struct.md
```

The documentation must describe:

- module ownership,
- allowed dependencies,
- forbidden dependencies,
- input → processing → output,
- `CapabilityTemplate`,
- `ConstraintScope`,
- `Capability`,
- structural invariants,
- policy consistency,
- risk consistency,
- approval requirements,
- constraint-scope behavior,
- domain/application boundary,
- and public interface.

The documentation must not introduce behavior that is absent from this specification.

---

## Public Interface

The module exposes:

```text
CapabilityTemplate
ConstraintScope
Capability
```

No runtime authorization API is exposed by this module.

No registry or repository API is exposed.

No persistence API is exposed.

---

## Implementation Constraints

- Use Pydantic for composite domain contracts.
- Use `Enum` types from shared vocabulary rather than duplicating vocabulary definitions.
- Use immutable/frozen contract semantics.
- Use explicit structural validators.
- Import `Operation` and `Interface` from `domain.vocabulary`.
- Import `Policy` and `PolicyVerdict` from `domain.policy`.
- Import `Risk`, `RiskLevel`, and `RiskMode` from `domain.risk`.
- No I/O.
- No filesystem access.
- No network access.
- No database access.
- No Redis access.
- No registry/repository access.
- No runtime authorization.
- No approval workflow.
- No policy mutation.
- No risk retrieval.
- No global mutable state.
- No metaprogramming.
- No speculative abstractions.
- Explicit behavior over clever abstractions.

---

## Files Permitted

Codex may create or modify only:

```text
D:\academic\Zenith\domain\capability.py
D:\academic\Zenith\domain\capability_struct.md
D:\academic\Zenith\tests\unit\domain\test_capability.py
```

Nothing else.

If anything in this specification is ambiguous, stop and ask rather than guessing.