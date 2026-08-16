# Module Specification — `domain/capability.py`

## Owns

- `CapabilityTemplate`
- `ConstraintScope`
- `Capability`

## Must NOT depend on

- `application/*`
- `infrastructure/*`
- `interface/*`

No I/O.

Imports shared vocabulary, Policy, and Risk domain contracts only.

## Authority Boundary

**MAY:**
- Validate structural consistency.
- Ensure prohibited policies cannot be active.
- Ensure high/critical explicit risk requires approval.
- Represent capability constraints.

**MUST NOT:**
- Perform runtime authorization.
- Query registries.
- Determine current registration status.
- Access databases or external systems.

## Invariants

1. `PROHIBITED` capability cannot be `ACTIVE`.
2. `HIGH` or `CRITICAL` explicit risk requires `requires_approval=True`.
3. `APPROVAL_REQUIRED` policy requires `requires_approval=True`.
4. Domain performs only structural validation.

## Contract Version

```text
CapabilityTemplate v1
ConstraintScope v1
Capability v1