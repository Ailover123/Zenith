# Module Specification — `domain/observation_event.py`

## Owns

- `ObservationEvent`

## Must NOT depend on

- Application
- Infrastructure
- Interface
- Redis
- Postgres

## Authority Boundary

Represents normalized external observations.

It does NOT interpret meaning.

It does NOT create Derived World Facts.

## Contract

```text
ObservationEvent
├── event_id
├── source
├── source_native_id
├── event_type
├── timestamp
├── subject
├── resource_key
├── raw_payload
├── normalized_payload
├── provenance
└── correlation_id