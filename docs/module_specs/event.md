# Module Specification — domain/event.py

# Status

READY FOR IMPLEMENTATION

# Version

1.0

# Tier

0

# Owns

This module owns the pure domain representation of an external world observation.

It owns:

- ObservationEvent

This module represents an observation entering Zenith from an external or internal source.

It does NOT own:

- connector implementations
- ingestion
- normalization
- event deduplication
- event ordering
- reconciliation
- persistence
- world-state updates
- task events
- security events
- runtime event processing

# Naming

The contract is named ObservationEvent.

It must not be named Event because Zenith distinguishes between multiple event concepts:

- ObservationEvent — external or observational input describing something observed in the world
- TaskEvent — internal task lifecycle or audit event
- SecurityEvent — security telemetry

ObservationEvent is specifically the domain contract for an observation entering the system.

# Must NOT depend on

This module must not depend on:

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
- runtime services
- repositories
- registries
- persistence systems
- databases
- Redis
- network clients
- external APIs
- filesystem interfaces
- connector implementations

No I/O.

No relative imports.

# Allowed Dependencies

Allowed dependencies are limited to:

- Python standard-library types and enums
- Pydantic for immutable domain contracts

ObservationEvent must remain independently representable.

Cross-contract references must use IDs or primitive immutable values.

# Authority Boundary

ObservationEvent represents an observation.

The domain model may:

- represent observation identity;
- represent observation source;
- represent source-native identity;
- represent event type;
- represent observation timestamp;
- represent the resource associated with the observation;
- preserve the raw payload supplied by ingestion;
- represent the normalized payload produced by deterministic ingestion logic;
- represent provenance;
- represent correlation information;
- validate structural consistency;
- enforce immutable contract semantics.

The domain model must NOT:

- retrieve external data;
- call connectors;
- normalize external data;
- infer normalized values;
- classify events using an LLM;
- deduplicate observations;
- query Redis;
- determine whether an event was already processed;
- determine event ordering;
- assign state versions;
- reconcile events;
- update World State;
- persist observations;
- execute capabilities;
- perform authorization;
- process TaskEvents;
- process SecurityEvents;
- access external systems.

# Input -> Processing -> Output

External observation data

+

Zenith-assigned event identity

+

Source identity

+

Source-native identity

+

Deterministic normalized payload

+

Provenance

+

Correlation information

        |

        v

structural validation

        |

        v

valid immutable ObservationEvent

Validation is strictly structural.

No external state is read.

No external state is modified.

No reconciliation is performed.

No authorization decision is produced.

# Public Contract

# ObservationEvent

ObservationEvent represents one observation entering Zenith.

It contains:

- event_id: str
- source: str
- source_native_id: str
- event_type: str
- timestamp: datetime
- resource_key: str
- raw_payload: object
- normalized_payload: dict[str, object]
- provenance: str
- correlation_id: str

ObservationEvent is a frozen Pydantic model.

All fields are part of the immutable observation record.

# Field Semantics

# event_id

event_id is the Zenith-generated identifier for this observation.

It is assigned by the ingestion/application layer before construction of the domain contract.

The domain model stores the identifier but does not generate it.

The domain model does not verify uniqueness.

Uniqueness and identifier generation belong to the application or ingestion layer.

# source

source identifies the system or actor from which the observation originated.

Examples include:

- gmail
- github
- calendar
- scheduled
- agent
- user

Source values are part of a connector/source vocabulary.

The domain model must not contain connector-specific semantic knowledge about which values are currently supported.

Source recognition and connector-specific vocabulary ownership belong to the ingestion/application layer.

The domain model only represents the supplied source identifier structurally.

# source_native_id

source_native_id identifies the observation in its originating system.

Examples include:

- Gmail message ID
- GitHub delivery ID
- Calendar event ID

The pair:

source + source_native_id

forms the source-level idempotency identity.

The ObservationEvent domain object does not perform the deduplication check.

The application or ingestion layer owns idempotency lookup and enforcement.

# event_type

event_type identifies the type of observation emitted by the source.

Event types are defined by the source or connector vocabulary.

The domain contract does not maintain a global list of connector-specific event types.

The domain model performs structural validation only.

If validation is applied, event_type must satisfy the structural requirement of being a non-empty snake_case identifier.

The domain model must NOT determine whether an event type is semantically recognized by Gmail, GitHub, Calendar, or another connector.

Semantic event-type recognition belongs to the corresponding ingestion/connector layer.

# Structural Versus Semantic Validation

ObservationEvent validation must remain structural.

Structural validation may verify properties such as:

- required identifiers are present;
- strings are structurally valid;
- event_type follows the required snake_case representation;
- timestamp has the correct type;
- payload fields have the required structural representation;
- immutable contract semantics are preserved.

Structural validation must NOT verify connector-specific semantics.

For example:

- The domain may verify that event_type is a valid snake_case string.
- The domain must not verify that message_received is a recognized Gmail event type.
- The domain must not maintain a Gmail event vocabulary.
- The domain must not maintain a GitHub event vocabulary.
- The domain must not inspect connector-specific payload semantics.

Adding a new connector must not require modification of ObservationEvent merely to add connector-specific event types.

# timestamp

timestamp represents the timestamp associated with the observation.

It is advisory metadata only.

timestamp must NEVER be used by ObservationEvent for event ordering.

The domain model does not determine event order.

Network delays, queue delays, retries, clock differences, and external-system behavior can cause timestamps to be unsuitable for authoritative ordering.

Ordering belongs to the application/reconciliation layer.

Zenith-assigned state_version is used when authoritative derived-state ordering is required.

# resource_key

resource_key identifies the logical resource associated with the observation.

It follows the same resource_key convention used by Resource Coordination.

The domain model stores the resource key as an identifier.

It does not resolve the resource.

It does not retrieve the resource.

It does not verify that the resource exists.

It does not determine resource ownership.

# raw_payload

raw_payload represents the original payload preserved by the ingestion layer.

The ObservationEvent domain model does not define how external data is converted, reshaped, serialized, decoded, or otherwise prepared before being supplied as raw_payload.

Whatever representation the ingestion layer has already decided to preserve as the raw payload is stored by ObservationEvent.

The domain model must not transform raw_payload.

The domain model must not normalize raw_payload.

The domain model must not interpret raw_payload.

The domain model must not use raw_payload for reasoning.

The domain model must not invoke an LLM on raw_payload.

Preservation and ingestion decisions belong to the ingestion/application layer.

# normalized_payload

normalized_payload contains the deterministic structured representation produced by source-specific ingestion logic.

Normalization is performed before the observation reaches reasoning.

Normalization must be deterministic code.

Normalization must NOT be performed by the LLM.

The domain model stores normalized_payload but does not produce it.

The domain model does not reinterpret or enrich normalized_payload.

Source-specific normalization logic belongs to the corresponding connector or ingestion layer.

# provenance

provenance records the origin or processing provenance associated with the observation.

It is represented as domain data.

The domain model stores provenance but does not independently verify its truth.

Provenance generation and verification belong to the ingestion/application layer.

ObservationEvent does not grant additional authority based on provenance.

# correlation_id

correlation_id associates the observation with a broader operation, workflow, request, or chain of related activity.

It is represented as an identifier.

The domain model does not resolve or retrieve the associated workflow.

The domain model does not infer relationships from correlation_id.

# Structural Invariants

1. ObservationEvent is immutable.

2. ObservationEvent uses a frozen Pydantic model.

3. event_id is represented as a Zenith-generated identifier string.

4. source is represented as an explicit source identifier.

5. source_native_id is represented as an explicit source-native identifier.

6. event_type is represented as an explicit string.

7. event_type structural validation is limited to the required identifier format.

8. event_type semantic recognition is owned by the source-specific ingestion layer.

9. timestamp is advisory metadata only.

10. timestamp is never used by ObservationEvent for ordering.

11. resource_key is represented as an identifier.

12. raw_payload is preserved exactly as supplied by the ingestion layer.

13. ObservationEvent does not reshape raw_payload.

14. ObservationEvent does not normalize raw_payload.

15. normalized_payload represents deterministic connector-produced normalization.

16. ObservationEvent does not perform normalization.

17. LLMs are never used by ObservationEvent for normalization.

18. provenance is represented as domain data.

19. correlation_id is represented as an identifier.

20. Cross-contract references use IDs or primitive immutable values.

21. ObservationEvent does not resolve external IDs.

22. ObservationEvent does not retrieve external state.

23. ObservationEvent does not query repositories or registries.

24. ObservationEvent does not perform idempotency checks.

25. ObservationEvent does not perform event ordering.

26. ObservationEvent does not assign state_version.

27. ObservationEvent does not reconcile observations.

28. ObservationEvent does not update World State.

29. ObservationEvent does not persist itself.

30. ObservationEvent performs no I/O.

31. ObservationEvent contains no global mutable state.

32. ObservationEvent does not perform authorization.

33. ObservationEvent does not execute capabilities.

34. ObservationEvent does not create TaskEvents.

35. ObservationEvent does not create SecurityEvents.

36. Cross-module dependencies remain within the declared domain boundary.

# Idempotency Boundary

The source and source-native identifier pair:

source + source_native_id

is the idempotency identity of an observation.

The ObservationEvent domain model does not determine whether that identity has already been observed.

Idempotency requires external state.

Therefore idempotency lookup belongs to the application/ingestion layer.

The application layer may query an idempotency store or repository and reject duplicate observations before or during event processing.

The domain object only represents the supplied identifiers.

# Ordering Boundary

ObservationEvent.timestamp is never an authoritative ordering mechanism.

Authoritative ordering belongs to Zenith-controlled state-versioning and reconciliation mechanisms.

The application/reconciliation layer is responsible for:

- receiving observations;
- determining processing order;
- assigning appropriate Zenith-controlled state versions;
- reconciling observations into derived state;
- constructing updated WorldStateEntity objects.

ObservationEvent itself does not perform ordering.

# Normalization Boundary

External observations must be normalized before they are consumed by reasoning systems.

Normalization is performed by deterministic source-specific code.

The LLM must not be responsible for normalization.

The ingestion layer is responsible for:

- receiving external data;
- preserving the raw payload;
- applying deterministic source-specific normalization;
- constructing the normalized payload;
- constructing the ObservationEvent.

ObservationEvent only represents the resulting data.

# Source Fact Boundary

A connector may produce an ObservationEvent and associated Source Facts.

A connector must never directly write an authoritative Derived World Fact.

Only the reconciliation/application layer may promote observed source information into authoritative Derived World State.

This prevents a connector from directly defining Zenith's worldview.

ObservationEvent therefore represents evidence entering the system, not authoritative world state.

# AI Collaboration Boundary

ObservationEvents originating from AI collaboration systems receive no elevated trust.

An ObservationEvent originating from an AI collaboration connector must pass through the same downstream reconciliation and plan-sanity mechanisms as observations from other sources.

The source being an AI system does not make the observation authoritative.

The domain model does not create a privileged AI source category.

# Provenance and Trust

Provenance describes where an observation came from.

Provenance does not itself create authorization.

Provenance does not make an observation authoritative.

Provenance does not bypass reconciliation.

Provenance does not bypass plan validation.

Trust decisions belong to higher-level application and security mechanisms.

# Replay Semantics

ObservationEvent is a historical observation record.

Replaying an ObservationEvent does not mutate the ObservationEvent itself.

Replay behavior belongs to the application/reconciliation layer.

The domain contract only represents the observation being replayed.

# Immutability

ObservationEvent uses frozen Pydantic semantics.

After construction:

- event_id cannot be reassigned;
- source cannot be reassigned;
- source_native_id cannot be reassigned;
- event_type cannot be reassigned;
- timestamp cannot be reassigned;
- resource_key cannot be reassigned;
- raw_payload cannot be reassigned;
- normalized_payload cannot be reassigned;
- provenance cannot be reassigned;
- correlation_id cannot be reassigned.

State changes or corrected observations must be represented by new domain objects rather than mutation of an existing ObservationEvent.

# Domain and Application Boundary

# Domain owns

- ObservationEvent representation
- Structural validation
- Immutable observation contracts
- Observation identifiers
- Source identifiers
- Event-type structural representation
- Timestamp representation
- Resource-key representation
- Raw payload representation
- Normalized payload representation
- Provenance representation
- Correlation representation

# Ingestion/Application owns

- Receiving external observations
- Connector execution
- Source-specific event-type vocabularies
- Source-specific semantic validation
- Raw payload preservation decisions
- Deterministic normalization
- Source-native deduplication
- Idempotency checks
- Event processing
- Event ordering
- State-version assignment
- Reconciliation
- Constructing updated WorldStateEntity objects
- Scope of downstream processing

# Infrastructure owns

- External system connectivity
- Connector infrastructure
- Redis access
- Databases
- Event persistence
- Idempotency stores
- Message queues
- Network communication

# Authorization owns

- Actor authorization
- Capability authorization
- Grant evaluation
- Delegation evaluation
- Approval requirements
- Runtime authorization enforcement

# What ObservationEvent Does NOT Own

ObservationEvent explicitly does NOT own:

- connector execution;
- external data retrieval;
- external API access;
- source-specific semantic validation;
- source-specific event vocabularies;
- payload normalization;
- LLM-based interpretation;
- idempotency;
- deduplication;
- event ordering;
- state-version assignment;
- reconciliation;
- World State mutation;
- persistence;
- authorization;
- capability execution;
- task execution;
- security decisions.

# Required Tests

The implementation must include tests covering at least:

- test_observation_event_is_structurally_valid()
- test_observation_event_is_frozen()
- test_event_id_is_stored_as_id()
- test_source_native_id_is_stored_as_id()
- test_event_type_accepts_structurally_valid_identifier()
- test_event_type_rejects_invalid_structure()
- test_timestamp_is_stored_as_advisory_metadata()
- test_resource_key_is_stored_as_identifier()
- test_raw_payload_is_preserved()
- test_normalized_payload_is_stored()
- test_provenance_is_stored()
- test_correlation_id_is_stored()
- test_source_and_source_native_id_are_represented()
- test_no_external_state_is_required()
- test_no_forbidden_layer_imports()
- test_no_relative_imports()

Tests must NOT require:

- Redis;
- databases;
- repositories;
- network access;
- connectors;
- external APIs;
- filesystem access;
- application services.

# Implementation Notes

The implementation must remain small and domain-pure.

Do not add:

- connector registries;
- event buses;
- repositories;
- normalization functions;
- deduplication methods;
- ordering methods;
- reconciliation methods;
- authorization methods;
- external integrations;
- LLM calls;
- global registries;
- mutable global state.

The domain contract should contain only the representation and structural validation required by this specification.

# Public Interface

The module exposes:

- ObservationEvent

# Contract Version

ObservationEvent v1