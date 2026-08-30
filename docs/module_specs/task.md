# Module Specification — domain/task.py

# Status

READY FOR IMPLEMENTATION

# Version

1.0

# Tier

0

# Module Ownership

This module owns the pure domain representation of task lifecycle state and task dormancy/resume configuration.

It owns:

- Task
- TaskEvent
- ResumeTrigger
- TaskStatus

This module represents what a Task is, its lifecycle state, its task-level event history contract, and the structural conditions under which a dormant task may be configured to resume.

It does NOT execute tasks, evaluate runtime triggers, retrieve World State, invoke capabilities, perform authorization, or persist task state.

# Allowed Dependencies

Allowed dependencies are limited to:

- Python standard-library types
- datetime
- enum.Enum
- Pydantic BaseModel
- Pydantic ConfigDict
- Pydantic Field

This module may depend on domain.scope.

Cross-contract references to other domain objects must use IDs rather than importing or embedding runtime objects.

# Forbidden Dependencies

This module must not import:

- application/*
- infrastructure/*
- interface/*
- domain.capability
- domain.authorization
- domain.policy
- domain.risk
- domain.worldstate
- domain.event
- domain.plan

It must not depend on:

- Runtime services
- Repositories
- Registries
- Databases
- Redis
- Network clients
- External APIs
- Filesystem interfaces
- Capability implementations
- Authorization engines
- Event processors
- World State retrieval systems

No relative imports are permitted.

# Dependency Boundary

Task is a domain lifecycle contract.

A Task may reference its declared DomainScope because scope is part of the task's structural declaration.

Task must not resolve or retrieve anything represented by an ID.

For example:

- task_id is an ID
- parent_task_id is an ID
- plan_id is an ID
- capability_id is an ID
- event IDs are IDs

The Task contract does not resolve these identifiers into runtime objects.

# Authority Boundary

The domain task model MAY:

- represent task identity;
- represent task lifecycle state;
- represent task scope;
- represent task-level lifecycle events;
- represent dormancy configuration;
- represent resume-trigger configuration;
- validate structural consistency;
- enforce immutable contract semantics;
- represent IDs linking a task to related domain contracts.

The domain task model MUST NOT:

- execute a task;
- execute a capability;
- authorize a task;
- evaluate authorization;
- retrieve World State;
- inspect current external state;
- evaluate a resume trigger against current time;
- evaluate a resume trigger against incoming events;
- schedule a task;
- wake a dormant task;
- persist task state;
- modify an existing task in place;
- invoke application services;
- query repositories;
- resolve IDs into objects;
- infer task state from external events.

Application/runtime layers own task orchestration and lifecycle transitions.

# Input -> Processing -> Output

Task declaration:

Task identity + scope + lifecycle configuration + declared metadata

↓

Pydantic structural validation

↓

valid immutable Task contract

Task event declaration:

Task event ID + task ID + event type + timestamp + event metadata

↓

Pydantic structural validation

↓

valid immutable TaskEvent contract

Resume configuration:

Resume trigger type + trigger configuration

↓

Pydantic structural validation

↓

valid immutable ResumeTrigger contract

# TaskStatus

TaskStatus represents the lifecycle state category of a Task.

It contains exactly:

- CREATED = "created"
- OBSERVING = "observing"
- PLANNING = "planning"
- REVALIDATING = "revalidating"
- ACTING = "acting"
- WAITING = "waiting"
- DELEGATED = "delegated"
- ASKING = "asking"
- SURFACED = "surfaced"
- COMPLETED = "completed"
- FAILED = "failed"
- ESCALATED_TO_HUMAN = "escalated_to_human"

TaskStatus is descriptive state only.

The enum does not perform lifecycle transitions.

The enum does not determine whether a transition is valid.

Transition orchestration belongs to the application/task runtime layer.

# ResumeTrigger

ResumeTrigger represents a structurally declared condition or signal that may be used by the application layer as a reason to reconsider a dormant Task.

ResumeTrigger does not evaluate the trigger.

ResumeTrigger does not inspect current time.

ResumeTrigger does not inspect events.

ResumeTrigger does not query World State.

ResumeTrigger does not schedule wake-ups.

ResumeTrigger represents configuration only.

ResumeTrigger contains:

- trigger_type: str
- configuration: dict[str, object]

trigger_type is a non-empty snake_case identifier.

The semantic meaning of trigger_type and the interpretation of configuration are owned by the application/runtime layer responsible for evaluating the trigger.

The domain contract must not contain connector-specific trigger registries or runtime trigger implementations.

# TaskEvent

TaskEvent represents one immutable task lifecycle or task-level audit entry.

TaskEvent contains:

- event_id: str
- task_id: str
- event_type: str
- timestamp: datetime
- details: dict[str, object]

event_id is the identifier of the TaskEvent.

task_id identifies the Task to which the event belongs.

event_type is a non-empty snake_case identifier.

event_type represents a structural event category only.

The domain contract does not maintain a registry of every possible task event type.

timestamp represents the time associated with the task event as metadata.

TaskEvent does not process events.

TaskEvent does not determine lifecycle transitions.

TaskEvent does not update the Task.

TaskEvent does not persist itself.

TaskEvent does not retrieve previous events.

# Task

Task represents one structured unit of work managed by the JARVIS task lifecycle.

Task contains:

- task_id: str
- scope: DomainScope
- status: TaskStatus
- created_at: datetime
- parent_task_id: str | None
- plan_id: str | None
- capability_id: str | None
- resume_trigger: ResumeTrigger | None

The Task contract may contain additional explicitly declared task metadata only if it is part of the locked contract. Do not invent runtime fields during implementation.

task_id is the unique identifier of the task.

scope is the task's explicitly declared DomainScope.

parent_task_id is an optional ID reference to a parent task.

plan_id is an optional ID reference to the plan associated with the task.

capability_id is an optional ID reference to the capability associated with the task.

resume_trigger is optional configuration for reconsidering a dormant or waiting task.

Task is a frozen Pydantic model.

# Task Structural Invariants

1. Task is immutable.

2. TaskStatus contains exactly the lifecycle states defined in this specification.

3. task_id is an explicit string identifier.

4. scope is an explicit DomainScope.

5. created_at is an explicit datetime.

6. parent_task_id is either an explicit string ID or None.

7. plan_id is either an explicit string ID or None.

8. capability_id is either an explicit string ID or None.

9. resume_trigger is either a ResumeTrigger contract or None.

10. Cross-contract references are represented using IDs or explicitly owned domain contracts.

11. Task does not resolve referenced IDs.

12. Task does not retrieve related plans, capabilities, events, authorization decisions, or world-state entities.

13. Task does not execute capabilities.

14. Task does not perform authorization.

15. Task does not evaluate resume conditions.

16. Task does not perform lifecycle transitions itself.

17. Task does not persist itself.

18. Task performs no I/O.

19. Task contains no global mutable state.

20. Task lifecycle orchestration remains outside the domain contract.

# Task Event Invariants

1. TaskEvent is immutable.

2. event_id is an explicit string identifier.

3. task_id is an explicit string identifier.

4. event_type is a non-empty snake_case identifier.

5. timestamp is represented as datetime metadata.

6. details is structured task-event data.

7. TaskEvent does not resolve task_id.

8. TaskEvent does not retrieve or inspect external state.

9. TaskEvent does not perform event processing.

10. TaskEvent does not determine lifecycle transitions.

11. TaskEvent does not persist itself.

12. TaskEvent performs no I/O.

# Resume Trigger Invariants

1. ResumeTrigger is immutable.

2. trigger_type is a non-empty snake_case identifier.

3. configuration is structured data.

4. ResumeTrigger does not evaluate trigger conditions.

5. ResumeTrigger does not inspect current time.

6. ResumeTrigger does not inspect incoming events.

7. ResumeTrigger does not retrieve World State.

8. ResumeTrigger does not schedule execution.

9. ResumeTrigger does not wake tasks.

10. Semantic interpretation of trigger_type is owned by the application/runtime layer.

11. No connector-specific runtime registry is owned by this domain contract.

12. ResumeTrigger performs no I/O.

# Lifecycle Semantics

TaskStatus describes the current lifecycle position of a Task.

The statuses represent:

CREATED

The Task exists but has not entered active observation or planning.

OBSERVING

The Task is in an observation/state-gathering phase.

PLANNING

The Task is being planned.

REVALIDATING

The Task's plan or intended execution is undergoing required revalidation.

ACTING

The Task is in an execution/acting phase.

WAITING

The Task is dormant or waiting for a condition, event, dependency, or external continuation.

DELEGATED

The Task has been delegated to another actor or execution path.

ASKING

The Task is waiting for required human or external input.

SURFACED

The Task has been surfaced for attention or decision.

COMPLETED

The Task has reached successful completion.

FAILED

The Task has reached a failed terminal state.

ESCALATED_TO_HUMAN

The Task requires human intervention or has been escalated to a human authority.

These descriptions are semantic documentation only.

The Task domain contract does not implement the state machine.

# Lifecycle Transition Boundary

TaskStatus does not determine whether one status may transition to another.

For example, the domain enum does not itself enforce:

CREATED -> OBSERVING

OBSERVING -> PLANNING

PLANNING -> REVALIDATING

REVALIDATING -> ACTING

ACTING -> COMPLETED

or any other transition.

Actual transition validity belongs to the task lifecycle/application layer.

This prevents the Tier-0 domain contract from silently becoming a task orchestration engine.

# Dormancy and Resume Boundary

WAITING and ASKING may represent states in which a Task is not currently progressing through active execution.

ResumeTrigger represents the declared configuration that may tell the application layer what kind of condition should cause the Task to be reconsidered.

The domain contract does not determine whether the condition has occurred.

The application layer is responsible for:

- receiving relevant events;
- observing current time where applicable;
- retrieving required external state;
- evaluating the configured trigger;
- determining whether the Task should resume;
- applying lifecycle transition rules;
- constructing the resulting Task representation.

# Scope Boundary

Task may contain a DomainScope because scope is part of the Task's declared domain boundary.

Task does not:

- expand scope;
- authorize scope;
- discover entities;
- retrieve World State;
- infer scope from events;
- modify the DomainScope in place.

Scope expansion remains an application-level, policy-gated operation as defined by domain.scope.

# Plan Boundary

plan_id is an ID reference only.

Task does not import or resolve Plan.

Task does not create plans.

Task does not execute plans.

Task does not determine whether a plan is valid.

Task does not revalidate plan assumptions.

Plan construction and reasoning belong to the planning/application layer.

# Capability Boundary

capability_id is an ID reference only.

Task does not import or resolve capability objects.

Task does not invoke capabilities.

Task does not authorize capability execution.

Capability lookup, authorization, execution, and failure handling belong to the appropriate runtime/application layers.

# Authorization Boundary

Task does not own authorization decisions.

Task does not contain grants, delegations, authorization verdicts, or approval workflows unless explicitly added later as ID references.

Task does not decide whether a task may execute.

Authorization belongs to the authorization layer.

# World State Boundary

Task does not retrieve or inspect World State.

Task does not infer its lifecycle from World State.

Task does not mutate World State.

Application/runtime orchestration may use World State to determine what should happen to a Task, but that behavior must remain outside this module.

# Event Boundary

TaskEvent represents task-local lifecycle/audit information.

It is distinct from ObservationEvent.

ObservationEvent represents an observation entering Zenith from an external or internal source.

TaskEvent represents a Task lifecycle or task-level audit entry.

TaskEvent must not import or become an alias for ObservationEvent.

TaskEvent does not process ObservationEvents.

Event processing and reconciliation belong outside this module.

# Persistence Boundary

Neither Task nor TaskEvent persists itself.

The application/infrastructure layers are responsible for:

- storing tasks;
- retrieving tasks;
- storing task events;
- retrieving task events;
- maintaining event history;
- coordinating task state updates.

The domain contracts only represent valid immutable values.

# Immutability

Task, TaskEvent, and ResumeTrigger use frozen Pydantic semantics.

After construction:

- Task fields cannot be reassigned.
- TaskEvent fields cannot be reassigned.
- ResumeTrigger fields cannot be reassigned.

Collection-like fields must use immutable tuple semantics where tuples are part of the contract.

Dictionary fields represent structured data supplied to the contract. The domain contract must not introduce mutation-oriented helper methods.

# Domain and Application Boundary

## Domain owns

- Task representation
- TaskEvent representation
- ResumeTrigger representation
- TaskStatus representation
- Structural validation
- Immutable task contracts
- Explicit ID references
- Declared task scope
- Declared resume configuration

## Application owns

- Task creation orchestration
- Task lifecycle transitions
- Trigger evaluation
- Resume decisions
- Task scheduling
- World State retrieval
- Event processing
- Plan creation and selection
- Capability selection
- Authorization requests
- Task execution orchestration
- Task persistence coordination

## Infrastructure owns

- Task repositories
- Task event repositories
- Persistence
- Databases
- Redis
- External system access
- Scheduling infrastructure
- Event transport

## Interface owns

- Receiving user or external task requests
- Presenting task state
- Presenting task outcomes
- Translating external requests into application commands

# What Task Does NOT Own

domain/task.py explicitly does NOT own:

- Capability execution
- Authorization
- Policy evaluation
- Risk evaluation
- World State retrieval
- World State reconciliation
- External observation ingestion
- ObservationEvent processing
- Plan generation
- Plan execution
- Task scheduling
- Resume-trigger evaluation
- Repository access
- Persistence
- Database or Redis access
- Network access
- Filesystem access
- External API access
- Global mutable task state

# Required Tests

The implementation must include tests covering at minimum:

- test_task_status_has_expected_values()
- test_resume_trigger_is_structurally_valid()
- test_resume_trigger_is_frozen()
- test_task_event_is_structurally_valid()
- test_task_event_is_frozen()
- test_task_is_structurally_valid()
- test_task_is_frozen()
- test_task_scope_uses_domain_scope()
- test_task_references_are_stored_as_ids()
- test_resume_trigger_does_not_evaluate_conditions()
- test_task_does_not_execute_capabilities()
- test_task_does_not_resolve_runtime_objects()
- test_no_forbidden_layer_imports()
- test_no_relative_imports()

Tests should verify structural contracts rather than runtime orchestration.

Tests must not require:

- databases;
- Redis;
- repositories;
- external APIs;
- network access;
- runtime services.

# Implementation Constraints

Implement only the contracts defined by this specification.

Do not add:

- helper services;
- repositories;
- registries;
- transition engines;
- trigger evaluators;
- schedulers;
- authorization logic;
- capability execution logic;
- event-processing logic;
- persistence logic;
- external integrations.

Do not import unrelated domain modules merely for convenience.

The only domain-module dependency permitted by this specification is domain.scope for the Task scope contract.

# Public Interface

The module exposes:

- Task
- TaskEvent
- ResumeTrigger
- TaskStatus

No other public runtime service or helper is required by this Tier-0 specification.

# Contract Version

Task Domain Contract v1.0