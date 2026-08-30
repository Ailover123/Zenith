# domain/event.py

## Module Ownership

This module owns the pure domain representation of an external world observation:

- ObservationEvent

This module represents an observation entering Zenith from an external or internal source. It does NOT own connector implementations, ingestion, normalization, event deduplication, event ordering, reconciliation, persistence, world-state updates, task events, security events, or runtime event processing.

## Allowed Dependencies

Allowed dependencies are limited to:

- Python standard-library types (datetime, 
e)
- Pydantic (BaseModel, ConfigDict, ield_validator) for immutable domain contracts

domain/event.py remains independently representable. It does not import authorization, capability, policy, risk, planning, task, world-state, application, infrastructure, or interface objects.

## Forbidden Dependencies

This module must not import:

- application/*
- infrastructure/*
- interface/*
- domain.worldstate
- domain.capability
- domain.policy
- domain.risk
- domain.scope
- domain.plan
- domain.task
- Runtime services, repositories, registries, persistence systems, databases, Redis, network clients, external APIs, filesystem interfaces, or connector implementations.

No relative imports are permitted.

## Input -> Processing -> Output

`	ext
External observation data + Zenith event ID + Source ID + Source-native ID + Normalized payload + Provenance + Correlation ID
                                          ↓
                             Pydantic contract validation
                                          ↓
                             valid immutable ObservationEvent
`

- Validation is strictly structural.
- Cross-contract references (event_id, source_native_id, 
esource_key, correlation_id) are represented as string identifiers.
- No external state is read or modified.
- No event deduplication, ordering, reconciliation, or persistence is performed.
- Performs no I/O.

## Public Contracts

### ObservationEvent

ObservationEvent represents one observation entering Zenith:

- event_id: str
- source: str
- source_native_id: str
- event_type: str (non-empty snake_case identifier)
- 	imestamp: datetime (advisory metadata only)
- 
esource_key: str
- 
aw_payload: object (preserved as supplied)
- 
ormalized_payload: dict[str, object]
- provenance: str
- correlation_id: str

ObservationEvent is a frozen Pydantic model (ConfigDict(frozen=True)).

## Structural Invariants

1. ObservationEvent is immutable (Frozen=True).
2. event_id is represented as a Zenith-generated identifier string.
3. source is represented as an explicit source identifier string.
4. source_native_id is represented as an explicit source-native identifier string.
5. event_type is represented as a non-empty snake_case identifier string.
6. event_type semantic recognition is owned by the source-specific ingestion layer.
7. 	imestamp is advisory metadata only and never used by ObservationEvent for ordering.
8. 
esource_key is represented as an identifier string.
9. 
aw_payload is preserved exactly as supplied by the ingestion layer without modification.
10. 
ormalized_payload represents deterministic connector-produced normalization.
11. provenance is represented as domain data string.
12. correlation_id is represented as an identifier string.
13. ObservationEvent performs no I/O and contains no global mutable state.
14. Cross-module dependencies remain within the declared domain boundary.

## Public Interface

The module exposes:

- ObservationEvent
