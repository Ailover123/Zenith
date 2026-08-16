# Module Specification — `domain/authorization.py`

## Owns

- `Verdict`
- `DecisionObject`
- `RootGrant`
- `DelegationScope`

## Must NOT depend on

- `application/*`
- `infrastructure/*`
- `interface/*`
- Runtime repositories or services

Use IDs for cross-contract references.

## Authority Boundary

**MAY:**
- Represent authorization decisions and authority scopes.
- Validate structural consistency.

**MUST NOT:**
- Perform authorization itself.
- Query current grants.
- Consume nonces.
- Persist approvals.
- Execute capabilities.

## Verdict

Must include:

```text
ALLOW
DENY
REQUIRE_APPROVAL
SECURITY_UNAVAILABLE
THROTTLED