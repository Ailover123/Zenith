# domain/worldstate.py

## Module Ownership

This module owns the pure domain representation of JARVIS's authoritative Derived World Fact state:

- `EntityType`
- `WorldStateEntity`

This module represents the structural form of known world-state facts. It does NOT own world-state reconciliation, persistence, retrieval, event processing, or external-state synchronization.

## Allowed Dependencies

Allowed dependencies are limited to:

- Python standard-library types and `enum.Enum`
- Pydantic (`BaseModel`, `ConfigDict`, `Field`) for immutable domain contracts

`domain/worldstate.py` remains independently representable. It does not import authorization, capability, policy, risk, planning, task, event-processing, application, infrastructure, or interface objects.

## Forbidden Dependencies

This module must not import:

- `application/*`
- `infrastructure/*`
- `interface/*`
- `domain.event`
- Event repositories, World State repositories, runtime services, registries, databases, Redis, network clients, external APIs, or filesystem interfaces.

No relative imports are permitted.

## Input -> Processing -> Output

```text
Entity ID + Entity Type + Current Derived State + State Version + Last Updated Event ID
                                          ↓
                             Pydantic contract validation
                                          ↓
                            valid immutable WorldStateEntity
```

- Validation is strictly structural.
- Cross-contract references (`entity_id`, `last_updated_event_id`) are represented strictly as string IDs.
- No external state is read or modified.
- No event reconciliation or persistence is performed.
- Performs no I/O.

## Public Contracts

### `EntityType`

`EntityType` represents the structural category of a world-state entity:

- `USER = "user"`
- `DEVICE = "device"`
- `SERVICE = "service"`
- `RESOURCE = "resource"`
- `DOCUMENT = "document"`
- `SYSTEM = "system"`

These values represent entity categories only. `EntityType` does not resolve, retrieve, or inspect entities.

### `WorldStateEntity`

`WorldStateEntity` represents one authoritative derived world-state fact:

- `entity_id: str`
- `entity_type: EntityType`
- `current_state: dict[str, object]`
- `state_version: int` (must be non-negative)
- `last_updated_event_id: str`

`WorldStateEntity` is a frozen Pydantic model (`ConfigDict(frozen=True)`). It represents a snapshot of derived state and does not perform state transitions itself.

## Structural Invariants

1. `WorldStateEntity` is immutable (`frozen=True`).
2. `EntityType` contains exactly `USER`, `DEVICE`, `SERVICE`, `RESOURCE`, `DOCUMENT`, and `SYSTEM`.
3. `entity_id` is an explicit identifier string.
4. `entity_type` is an explicit `EntityType`.
5. `current_state` contains the currently derived state associated with the entity as a dictionary mapping string keys to state values.
6. `state_version` represents the version of the derived snapshot and must be a non-negative integer (`>= 0`).
7. `last_updated_event_id` is an explicit event identifier string.
8. `entity_id` and `last_updated_event_id` are represented as IDs rather than retrieved runtime objects.
9. The domain model does not retrieve, inspect, or verify the existence of the referenced event or entity.
10. The domain model does not update `state_version` or modify `current_state`.
11. The domain model does not reconcile events or persist world state.
12. The domain model performs no I/O and contains no global mutable state.
13. Cross-module dependencies remain within the declared domain boundary.

## State Semantics

`current_state` represents the currently derived state known for the entity as data only. The contract does not define how that state was produced, calculate state from events, infer missing state, query external systems, merge external state, or execute state transitions.

## State Version Semantics

`state_version` identifies the version of the derived state snapshot. The domain contract validates that the version is non-negative. Version incrementing, comparison, conflict resolution, and concurrency control belong to the reconciliation/application layer.

## Event Reference Semantics

`last_updated_event_id` identifies the event associated with the latest derived state represented by the entity as an ID reference only. `WorldStateEntity` does not import `domain.event`, retrieve the event, or process events.

## Immutability

`WorldStateEntity` uses frozen Pydantic semantics (`ConfigDict(frozen=True)`). After construction, no field can be reassigned. State changes produce a new valid domain representation rather than mutating an existing instance.

## Reconciliation Boundary

Reconciliation is responsible for converting incoming events and existing world-state information into updated derived state:
- receiving state-changing events;
- determining the affected entity;
- calculating the next derived state;
- determining the next state version;
- constructing a new `WorldStateEntity`;
- persisting the resulting state.

`WorldStateEntity` only represents the resulting valid state.

## Domain and Application Boundary

### Domain owns:
- `EntityType` representation
- `WorldStateEntity` representation
- Structural validation
- Immutable world-state snapshots
- Explicit entity and event ID representations
- Structural state-version validation

### Application owns:
- Deciding when world state must be retrieved
- Coordinating reconciliation and state updates
- Deciding which events affect which entities
- Constructing new world-state snapshots
- Integrating world state with tasks, plans, policies, or authorization

### Infrastructure owns:
- World-state persistence and repository implementations
- Database and Redis access
- External system synchronization
- Event storage and retrieval

### Interface owns:
- Receiving external requests
- Presenting world-state information
- Translating external input into application requests

## Event Boundary

`WorldStateEntity` does not process events. Events may cause new snapshots to be constructed by the reconciliation layer, but the domain model remains independent of event processing.

## Authorization Boundary

World state is descriptive domain state. `WorldStateEntity` does not authorize access, create grants, evaluate delegations, approve actions, or determine capability permissions. Authorization belongs entirely to the authorization layer.

## Capability and Task Boundary

`WorldStateEntity` does not own capabilities, plans, tasks, task scope, authorization decisions, or execution.

## What World State Does NOT Own

`domain/worldstate.py` explicitly does NOT own:
- Event processing and reconciliation
- Persistence, repositories, registries
- External-state retrieval, external APIs, network, filesystem, database, Redis access
- Authorization or capability execution
- Task planning, task execution, or scope expansion
- Runtime state synchronization

## Public Interface

The module exposes:

- `EntityType`
- `WorldStateEntity`
