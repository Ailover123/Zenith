# Module Specification — `domain/risk.py`

## Owns

- `Risk`
- `RiskMode`
- `RiskLevel`
- `effective_risk_level()`

Pure risk representation and resolution only.

## Must NOT depend on

- `application/*`
- `infrastructure/*`
- `interface/*`
- `domain/capability.py`
- `domain/policy.py`
- `domain/authorization.py`

No I/O, database, Redis, network, or filesystem access.

## Authority Boundary

**MAY:**
- Represent risk levels and modes.
- Validate structural consistency.
- Resolve effective risk from supplied `Risk` objects.
- Detect cycles and fail loudly.
- Resolve unknown references conservatively.

**MUST NOT:**
- Retrieve related risks itself.
- Query registries or repositories.
- Perform authorization.
- Decide approval requirements.
- Persist state.
- Modify policies.

## Contract

### `RiskLevel`

```text
LOW
MEDIUM
HIGH
CRITICAL