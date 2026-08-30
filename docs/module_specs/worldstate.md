# Module Specification — `domain/worldstate.py`

# Status

READY FOR IMPLEMENTATION

# Version

1.0

# Tier

0

---

# Owns

This module owns the pure domain representation of JARVIS's authoritative Derived World Fact state.

It owns:

- `WorldStateEntity`
- `EntityType`

This module represents the structural form of known world-state facts.

It does NOT own world-state reconciliation, persistence, retrieval, event processing, or external-state synchronization.

---

# Must NOT depend on

This module must not depend on:

- `application/*`
- `infrastructure/*`
- `interface/*`
- `domain.event`
- Event repositories
- World State repositories
- Runtime services
- Registries
- Databases
- Redis
- Network clients
- External APIs
- Filesystem interfaces

No I/O.

No relative imports.

---

# Allowed Dependencies

Allowed dependencies are limited to:

- Python standard-library types and enums
- Pydantic for immutable domain contracts

`domain/worldstate.py` must remain independently representable.

It must not import authorization, capability, policy, risk, planning, task, event-processing, application, infrastructure, or interface objects.

---

# Authority Boundary

`WorldStateEntity` represents JARVIS's authoritative Derived World Fact state.

The domain model may:

- represent world-state entities;
- represent entity types;
- validate structural consistency;
- enforce immutable contract semantics;
- preserve state-version information;
- preserve the event identifier from which the current derived state was produced.

The domain model must NOT:

- retrieve world state;
- update world state;
- reconcile events;
- consume events;
- process events;
- query repositories;
- query registries;
- access external systems;
- persist state;
- infer state from external systems;
- mutate an existing entity;
- perform authorization;
- execute capabilities.

Reconciliation owns actual state updates and persistence.

---

# Input -> Processing -> Output

```text
Entity ID
+
Entity Type
+
Current Derived State
+
State Version
+
Last Updated Event ID
        |
        v
structural validation
        |
        v
valid immutable WorldStateEntity

# Public Contracts

# EntityType

`EntityType` represents the structural category of a world-state entity.

The initial contract defines exactly:

- `USER`
- `DEVICE`
- `SERVICE`
- `RESOURCE`
- `DOCUMENT`
- `SYSTEM`

These values represent entity categories only.

`EntityType` does not resolve, retrieve, or inspect entities.

# WorldStateEntity

`WorldStateEntity` represents one authoritative derived world-state fact.

Fields:

- `entity_id: str`
- `entity_type: EntityType`
- `current_state: dict[str, object]`
- `state_version: int`
- `last_updated_event_id: str`

`WorldStateEntity` is a frozen Pydantic model.

The model represents a snapshot of derived state.

It does not perform state transitions itself.

# Structural Invariants

1. `WorldStateEntity` is immutable.

2. `EntityType` contains exactly the contract-defined entity types.

3. `entity_id` is an explicit identifier.

4. `entity_type` is an explicit `EntityType`.

5. `current_state` contains the currently derived state associated with the entity.

6. `current_state` is represented as a mapping of string keys to state values.

7. `state_version` represents the version of the derived world-state snapshot.

8. `state_version` must be a non-negative integer.

9. `last_updated_event_id` identifies the event associated with the latest derived state.

10. `entity_id` is represented by an ID rather than a retrieved runtime object.

11. `last_updated_event_id` is represented by an ID rather than a retrieved event object.

12. The domain model does not retrieve the event referenced by `last_updated_event_id`.

13. The domain model does not verify that the referenced event exists.

14. The domain model does not update `state_version`.

15. The domain model does not modify `current_state`.

16. The domain model does not reconcile events.

17. The domain model does not persist world state.

18. The domain model performs no I/O.

19. The domain model contains no global mutable state.

20. Cross-module dependencies remain within the declared domain boundary.

# State Semantics

`current_state` represents the currently derived state known for the entity.

It is data only.

The `WorldStateEntity` contract does not define how that state was produced.

The module must not:

- calculate state from events;
- infer missing state;
- query external systems;
- merge external state;
- execute state transitions;
- interpret business workflows.

Those responsibilities belong to higher-level reconciliation and application components.

# State Version Semantics

`state_version` identifies the version of the derived state snapshot.

The domain contract only validates that the version is structurally valid and non-negative.

The domain model does not:

- increment versions;
- compare versions from external sources;
- resolve version conflicts;
- decide which version is authoritative;
- perform optimistic concurrency control.

Version progression and reconciliation semantics belong to the reconciliation/application layer.

# Event Reference Semantics

`last_updated_event_id` identifies the event associated with the latest derived state represented by the entity.

It is an ID reference only.

`WorldStateEntity` must not:

- import `domain.event`;
- retrieve the event;
- inspect the event;
- validate event existence;
- process the event;
- derive state from the event.

Event retrieval and event processing belong outside this domain contract.

# Immutability

`WorldStateEntity` uses frozen Pydantic semantics.

After construction:

- `entity_id` cannot be reassigned;
- `entity_type` cannot be reassigned;
- `current_state` cannot be reassigned;
- `state_version` cannot be reassigned;
- `last_updated_event_id` cannot be reassigned.

The domain contract represents a state snapshot.

State changes must produce a new valid domain representation rather than mutating an existing instance.

# Reconciliation Boundary

Reconciliation is responsible for converting incoming events and existing world-state information into updated derived state.

Reconciliation owns:

- receiving state-changing events;
- determining the affected entity;
- calculating the next derived state;
- determining the next state version;
- constructing a new `WorldStateEntity`;
- persisting the resulting state;
- handling reconciliation failures;
- coordinating repository access.

`WorldStateEntity` only represents the resulting valid state.

# Domain and Application Boundary

# Domain owns

- `EntityType` representation;
- `WorldStateEntity` representation;
- structural validation;
- immutable world-state snapshots;
- explicit entity IDs;
- explicit event IDs;
- structural state-version validation.

# Application owns

- deciding when world state must be retrieved;
- coordinating reconciliation;
- deciding which events affect which entities;
- coordinating state updates;
- deciding when a new world-state snapshot is constructed;
- integrating world state with tasks, plans, policies, or authorization.

# Infrastructure owns

- world-state persistence;
- repository implementations;
- database access;
- Redis access;
- external system synchronization;
- event storage and retrieval.

# Interface owns

- receiving external requests;
- presenting world-state information;
- translating external input into application requests.

# Event Boundary

`WorldStateEntity` does not process events.

Events may cause a new world-state snapshot to be constructed by the reconciliation layer, but the world-state domain model itself remains independent of event processing.

No event repository or event-processing dependency is permitted.

# Authorization Boundary

World state is descriptive domain state.

`WorldStateEntity` does not determine whether an actor may access, modify, or act upon an entity.

Authorization belongs to the authorization layer.

World state must not:

- authorize access;
- create grants;
- evaluate delegations;
- approve actions;
- determine capability permissions.

# Capability and Task Boundary

`WorldStateEntity` does not own:

- capabilities;
- plans;
- tasks;
- task scope;
- authorization decisions;
- execution.

Other domain contracts may reference entity IDs where appropriate, but `WorldStateEntity` must remain independent of those contracts.

# What World State Does NOT Own

`domain/worldstate.py` explicitly does NOT own:

- event processing;
- event reconciliation;
- persistence;
- repositories;
- registries;
- external-state retrieval;
- external APIs;
- network access;
- filesystem access;
- database access;
- Redis access;
- authorization;
- capability execution;
- task planning;
- task execution;
- scope expansion;
- runtime state synchronization.

# Public Interface

The module exposes:

- `EntityType`
- `WorldStateEntity`

No additional public runtime services are required.

# Required Tests

The implementation must include tests covering:

- `test_entity_type_has_expected_values()`
- `test_world_state_entity_is_structurally_valid()`
- `test_world_state_entity_is_frozen()`
- `test_state_version_must_be_non_negative()`
- `test_current_state_is_represented_as_mapping()`
- `test_event_reference_is_stored_as_id()`
- `test_entity_id_is_stored_as_id()`
- `test_no_forbidden_layer_imports()`
- `test_no_relative_imports()`

Tests must verify the declared domain boundary.

Tests must not require repositories, databases, Redis, external APIs, network access, or filesystem interfaces.

# Contract Version

`EntityType v1`

`WorldStateEntity v1`