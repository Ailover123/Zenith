# domain/scope.py

## Module Ownership

This module owns the pure domain representation of the declared scope of a Task:

- `DomainScope`

The module represents what domain and entity boundaries a Task is explicitly declared to operate within. It is a pure Tier-0 domain contract and does NOT perform authorization or scope expansion.

## Allowed Dependencies

Allowed dependencies are limited to:

- Python standard-library types
- Pydantic (`BaseModel`, `ConfigDict`) for immutable domain contracts

`DomainScope` remains independently representable and does not depend on runtime world-state objects, repositories, or registries.

## Forbidden Dependencies

This module must not import:

- `application/*`
- `infrastructure/*`
- `interface/*`
- `domain.worldstate`
- World State repositories, registries, repositories, databases, Redis, network clients, external APIs, or filesystem interfaces.

No relative imports are permitted.

## Input -> Processing -> Output

```text
Allowed Entity Types + Allowed Domains + Boundaries
                         ↓
            Pydantic contract validation
                         ↓
             valid immutable DomainScope
```

- Validation is strictly structural.
- Cross-contract or external entity references are represented using IDs or primitive immutable values.
- No external state is read or modified.
- No authorization decision or scope expansion is produced.
- Performs no I/O.

## Public Contracts

### `DomainScope`

`DomainScope` represents the explicit domain boundary within which a Task is declared to operate:

- `allowed_entity_types: tuple[str, ...]` (default: `()`)
- `allowed_domains: tuple[str, ...]` (default: `()`)
- `boundaries: tuple[str, ...]` (default: `()`)

`DomainScope` is a frozen Pydantic model (`ConfigDict(frozen=True)`).

All collection fields use immutable tuple semantics.

## Structural Invariants

1. `DomainScope` is explicit and structured.
2. `DomainScope` is immutable (`frozen=True`).
3. Entity types, domains, and boundaries are represented explicitly as tuples of strings.
4. All collection fields default to empty tuples `()`.
5. Empty dimensions represent no additional restriction declared for that specific dimension.
6. Empty dimensions do not authorize external discovery or entity retrieval.
7. Scope validation is structural only and performs no I/O.
8. Scope validation does not query World State, repositories, or registries.
9. Reasoning or execution logic cannot directly modify a `DomainScope`.
10. Scope expansion is outside the authority of `DomainScope`.
11. `DomainScope` does not perform authorization.
12. `DomainScope` does not retrieve entities.
13. `DomainScope` does not infer scope from events.
14. `DomainScope` contains no global mutable state.
15. Cross-module dependencies remain within the declared domain boundary.

## Immutability

`DomainScope` uses frozen Pydantic semantics (`ConfigDict(frozen=True)`).
After construction:
- `allowed_entity_types` cannot be reassigned.
- `allowed_domains` cannot be reassigned.
- `boundaries` cannot be reassigned.

The underlying collections use immutable tuple semantics. No global mutable scope state exists.

## Explicit Scope Semantics

`DomainScope` represents explicitly declared domain boundaries. Cross-contract or external entity references must be represented using string identifiers or primitive immutable values rather than retrieved runtime objects.

## Empty-Dimension Semantics

An empty dimension (i.e. `()`) indicates that no additional structural restriction is declared for that particular dimension. An empty dimension is never interpreted by `DomainScope` as permission to discover or retrieve arbitrary external entities.

## Scope-Expansion Boundary

Reasoning and execution logic must not directly mutate or expand `DomainScope`. Scope expansion is an application-level, policy-gated operation.
The application layer is responsible for:
- receiving a scope-expansion request;
- determining why expansion is needed;
- applying applicable policy;
- obtaining required authorization or approval;
- constructing the resulting new `DomainScope`;
- deciding whether the expanded scope may be used.

`DomainScope` only represents the resulting declared boundary.

## World State Boundary

`DomainScope` does not depend on World State. It does not:
- query World State;
- discover entities;
- resolve entity IDs;
- inspect current entity state;
- infer scope from world-state data.

World State retrieval and entity resolution belong outside the domain scope contract.

## Event Boundary

`DomainScope` does not infer, adapt, or mutate scope based on events. Event processing and orchestration are owned by higher layers.

## Domain and Application Boundary

### Domain owns:
- `DomainScope` representation
- Explicit scope structure
- Structural validation
- Immutability enforcement
- Deterministic representation of declared boundaries

### Application owns:
- Retrieving relevant external state
- Determining which entities or domains are relevant
- Receiving scope-expansion requests
- Applying policy to scope expansion
- Requesting authorization or approval for expansion
- Constructing a new scope after an approved expansion
- Deciding when a scope is used

### Authorization owns:
- Evaluating actor authorization to operate within or expand scope
- Deciding whether access to a given entity or domain is permitted

### Infrastructure owns:
- Persistence
- Repository access
- World State retrieval
- External system access

### Interface owns:
- Receiving user or external requests
- Presenting scope information
- Translating external input into application requests

## What Scope Does NOT Own

`DomainScope` explicitly does NOT own:
- Authorization decisions or policy evaluation
- Scope expansion logic or approval workflows
- Entity discovery or resolution
- Repository or registry queries
- World State or event processing
- I/O, network, filesystem, database, or Redis operations

## Public Interface

The module exposes:

- `DomainScope`
