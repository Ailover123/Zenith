# domain/authorization.py

## Module Ownership

This module owns the pure domain representation of authorization decisions and authority scopes:

- `Verdict`
- `DecisionObject`
- `RootGrant`
- `DelegationScope`

This module represents authorization-related domain contracts. It is a pure contract module and does NOT perform authorization, execute approval workflows, or enforce runtime throttling.

## Allowed Dependencies

Allowed dependencies are limited to:

- Python standard-library types and `enum.Enum`
- Pydantic (`BaseModel`, `ConfigDict`) for immutable domain contracts

## Forbidden Dependencies

This module must not import:

- `application/*`
- `infrastructure/*`
- `interface/*`
- `domain.capability`
- `domain.policy`
- `domain.risk`
- Runtime repositories, runtime services, registries, persistence systems, databases, Redis, network clients, external APIs, or filesystem interfaces.

No relative imports are permitted.

## Input -> Processing -> Output

```text
Subject ID + Capability ID + Verdict + Reason
                     ↓
         Pydantic contract validation
                     ↓
        valid immutable DecisionObject
```

```text
Subject ID + Capability ID + Optional DelegationScope
                     ↓
         Pydantic contract validation
                     ↓
          valid immutable RootGrant
```

- Invalid structural state fails during construction with an explicit validation error (`ValidationError`).
- Cross-contract references are represented strictly as IDs.
- No external state is read or modified.
- No runtime authorization decision is evaluated by this module.

## Public Contracts

### `Verdict`

`Verdict` represents the outcome category of an authorization evaluation:

- `ALLOW = "allow"`
- `DENY = "deny"`
- `REQUIRE_APPROVAL = "require_approval"`
- `SECURITY_UNAVAILABLE = "security_unavailable"`
- `THROTTLED = "throttled"`

### `DelegationScope`

`DelegationScope` represents the structural boundaries within which authority may be delegated:

- `capability_ids: tuple[str, ...]` (default: `()`)
- `subject_ids: tuple[str, ...]` (default: `()`)

Both collections default to empty tuples. An empty collection imposes no additional structural restriction along that dimension.

`DelegationScope` is a frozen Pydantic model.

### `DecisionObject`

`DecisionObject` represents the immutable result of an authorization evaluation:

- `id: str`
- `subject_id: str`
- `capability_id: str`
- `verdict: Verdict`
- `reason: str`

`DecisionObject` is a frozen Pydantic model. It represents a result; it does not evaluate authorization.

### `RootGrant`

`RootGrant` represents a root authority grant from which authority may originate:

- `id: str`
- `subject_id: str`
- `capability_id: str`
- `scope: DelegationScope | None = None`

`RootGrant` is a frozen Pydantic model.

## Structural Invariants

1. `Verdict` contains exactly `ALLOW`, `DENY`, `REQUIRE_APPROVAL`, `SECURITY_UNAVAILABLE`, and `THROTTLED`.
2. `DecisionObject` is immutable.
3. `RootGrant` is immutable.
4. `DelegationScope` is immutable.
5. Required IDs must be structurally present.
6. Required reason must be structurally present on `DecisionObject`.
7. Cross-contract references remain string IDs.
8. Empty delegation-scope dimensions impose no additional structural restriction.
9. `DecisionObject` represents an authorization result but does not perform authorization.
10. `RootGrant` represents authority but does not verify runtime registration or validity.
11. `DelegationScope` represents authority boundaries but does not evaluate runtime authorization.
12. `SECURITY_UNAVAILABLE` remains distinct from `ALLOW`.
13. `REQUIRE_APPROVAL` does not execute an approval workflow.
14. `THROTTLED` does not perform throttling.
15. The module performs no I/O.
16. The module contains no global mutable state.
17. The module has no application, infrastructure, interface, or other domain module dependencies.

## Immutability

All authorization domain contracts use frozen Pydantic semantics (`ConfigDict(frozen=True)`). No contract exposes mutable global state.

## ID-Based References

All cross-contract relationships are represented using IDs (`subject_id`, `capability_id`, `capability_ids`, `subject_ids`). No domain objects (`Capability`, `Policy`, `Risk`, `User`) or runtime services are embedded.

## Domain and Application Boundary

### Domain owns:
- `Verdict` vocabulary
- Authorization decision representation (`DecisionObject`)
- Root-grant representation (`RootGrant`)
- Delegation-scope representation (`DelegationScope`)
- Structural validation of contracts
- Immutability enforcement

### Application owns:
- Retrieving grants and delegation information
- Determining which authority records are relevant
- Supplying authorization inputs
- Orchestrating authorization evaluation and approval workflows
- Nonce lifecycle and runtime registration checks

### Authorization Runtime owns:
- Evaluating whether a subject is authorized
- Evaluating grants and delegation scopes against requests
- Emitting the appropriate `DecisionObject`
- Enforcing authorization decisions

## Security-Unavailable Boundary

`SECURITY_UNAVAILABLE` is represented as a distinct verdict to ensure that failure to establish security state is never treated as permission. This module only represents the verdict value; the runtime authorization layer determines when to emit it.

## Approval Boundary

`REQUIRE_APPROVAL` represents an authorization result that requires approval. This module does not create approval requests, persist approvals, notify humans, wait for approval, or consume approval tokens.

## Throttling Boundary

`THROTTLED` represents an authorization result blocked by rate or resource constraints. This module does not track counters, consume tokens, check rate limits, or access databases/Redis.

## Runtime Authorization Notice

`domain/authorization.py` is strictly a pure domain contract module. Runtime authorization evaluation is entirely outside this module.

## Public Interface

The module exposes:

- `Verdict`
- `DecisionObject`
- `RootGrant`
- `DelegationScope`
