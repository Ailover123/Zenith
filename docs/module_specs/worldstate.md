# Module Specification — `domain/worldstate.py`

## Owns

- `WorldStateEntity`
- `EntityType`

## Must NOT depend on

- Application
- Infrastructure
- Interface
- Event repositories

## Authority Boundary

Represents JARVIS's authoritative Derived World Fact state.

The domain model validates structure only.

Reconciliation owns actual state updates and persistence.

## Contract

```text
WorldStateEntity
├── entity_id
├── entity_type
├── current_state
├── state_version
└── last_updated_event_id