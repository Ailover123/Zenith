# Module Specification — domain/plan.py

# Status

READY FOR IMPLEMENTATION

# Version

1.0

# Tier

0

# Owns

This module owns the pure domain representation of a structured reasoning plan.

It owns:

- Plan
- PlanOutcome

This module represents what a reasoning process intends to accomplish and the structural outcome of that plan.

It does NOT execute plans or actions.

# Must NOT depend on

This module must not depend on:

- application/*
- infrastructure/*
- interface/*
- domain.capability
- domain.task
- runtime authorization services
- runtime repositories
- registries
- databases
- Redis
- network clients
- external APIs
- filesystem interfaces
- execution engines
- planning services

No relative imports are permitted.

No I/O.

Cross-contract references must use IDs or primitive values.

# Allowed Dependencies

Allowed dependencies are limited to:

- Python standard-library types
- Pydantic BaseModel
- Pydantic ConfigDict
- Pydantic Field where structural constraints require it

Plan must remain independently representable.

It must not import capability objects, task objects, world-state objects, authorization objects, or runtime services.

# Authority Boundary

Plan represents a structured reasoning plan.

The domain model may:

- represent plan identity;
- represent the task associated with a plan;
- represent when the plan was created;
- represent the information the plan was based on;
- represent assumptions;
- represent constraints;
- represent validity conditions;
- represent the intended action;
- represent plan supersession relationships;
- represent the outcome of a plan;
- validate structural consistency;
- enforce immutable contract semantics.

The domain model must NOT:

- execute actions;
- execute capabilities;
- retrieve world state;
- query repositories;
- revalidate current world state;
- authorize capabilities;
- decide whether a plan may execute;
- determine runtime capability availability;
- resolve task objects;
- resolve capability objects;
- mutate an existing plan;
- perform approval workflows;
- persist plans;
- call external systems.

Planning, authorization, validation against current state, and execution belong to higher layers.

# Input -> Processing -> Output

Plan inputs:

Plan ID
+
Task ID
+
Creation timestamp
+
Basis of planning
+
Assumptions
+
Constraints
+
Validity conditions
+
Intended action
+
Supersession relationships
+
Plan outcome

        |
        v

Pydantic structural validation

        |
        v

valid immutable Plan

Validation is structural only.

The plan contract does not determine whether the represented plan is actually safe, authorized, executable, or still valid against current world state.

# Public Contracts

# Plan

Plan represents one structured reasoning plan associated with a Task.

Required fields:

- plan_id: str
- task_id: str
- created_at: datetime
- based_on: tuple[str, ...]
- assumptions: tuple[str, ...]
- constraints: tuple[str, ...]
- validity_conditions: tuple[str, ...]
- intended_action: str
- supersedes: str | None
- superseded_by: str | None
- outcome: PlanOutcome

Plan is a frozen Pydantic model using ConfigDict(frozen=True).

All collection fields use immutable tuple semantics.

Cross-contract references such as task_id and supersession references are represented using IDs rather than imported domain objects.

# PlanOutcome

PlanOutcome represents the structural outcome state of a plan.

The outcome must be represented using a fixed domain vocabulary rather than arbitrary free text.

The exact outcome vocabulary must remain limited to the values defined by this contract.

Recommended fixed values:

- PENDING
- COMPLETED
- FAILED
- SUPERSEDED
- ABORTED

PlanOutcome represents plan lifecycle outcome only.

It does not represent:

- authorization;
- capability execution success;
- security approval;
- world-state reconciliation;
- external system success.

Those concerns belong to their respective layers.

# Structural Invariants

1. Plan is immutable.

2. Plan uses ConfigDict(frozen=True).

3. plan_id is an explicit plan identifier string.

4. task_id is an explicit Task identifier string.

5. Plan does not import or contain a Task object.

6. created_at is represented using datetime.

7. created_at represents when the plan was created and is descriptive metadata.

8. based_on contains explicit references to information or state identifiers used when constructing the plan.

9. assumptions contains explicit structural descriptions of assumptions used by the reasoning process.

10. constraints contains explicit structural descriptions of constraints applicable to the plan.

11. validity_conditions contains explicit conditions under which the plan is considered structurally intended to remain applicable.

12. intended_action is represented as structured domain data describing the action the plan intends to perform.

13. Plan does not execute intended_action.

14. Plan does not determine whether intended_action is authorized.

15. Plan does not determine whether intended_action is currently executable.

16. supersedes is either null or an explicit plan identifier.

17. superseded_by is either null or an explicit plan identifier.

18. Supersession references use IDs and do not retrieve referenced plans.

19. outcome represents the plan's declared lifecycle outcome.

20. Plan does not independently transition its own outcome.

21. Plan does not inspect current world state to determine validity.

22. Plan does not revalidate assumptions or validity conditions against external state.

23. Plan does not perform authorization.

24. Plan does not execute capabilities.

25. Plan performs no I/O.

26. Plan contains no global mutable state.

27. Cross-module dependencies remain within the declared domain boundary.

# Collection Semantics

The following fields use immutable tuples:

- based_on
- assumptions
- constraints
- validity_conditions

These fields represent ordered structural information supplied when the plan is constructed.

The Plan domain contract does not append, remove, reorder, or otherwise mutate these collections.

A changed plan must be represented as a new Plan instance.

# Based-On Semantics

based_on represents the identifiers or references to information that the reasoning process used when constructing the plan.

These references are represented as strings.

The Plan domain model does not:

- retrieve the referenced information;
- verify that referenced information exists;
- query World State;
- query repositories;
- determine whether the referenced information is current.

Determining whether the information remains current belongs to the application/runtime layer.

# Assumption Semantics

assumptions represents explicit assumptions used by the reasoning process.

The domain contract stores these assumptions as data.

It does not determine whether an assumption is true.

It does not retrieve evidence to validate an assumption.

It does not use an LLM or external system to validate assumptions.

Assumption validation against current state belongs outside Plan.

# Constraint Semantics

constraints represents explicit constraints that the plan is expected to respect.

Constraints are represented as domain data.

Plan does not enforce execution-time constraints.

Application, authorization, policy, and execution layers are responsible for enforcing applicable constraints when the plan is evaluated or executed.

# Validity-Condition Semantics

validity_conditions represents explicit conditions under which the plan is intended to remain applicable.

These conditions are represented as structural data only.

Plan does not:

- evaluate external conditions;
- retrieve current state;
- determine whether conditions are currently satisfied;
- automatically invalidate itself.

Current validity evaluation belongs to the application/runtime layer.

# Intended Action Semantics

intended_action represents what the plan intends to accomplish.

It is descriptive plan data.

The field does not execute anything.

It does not directly contain a runtime capability object.

It does not authorize execution.

It does not guarantee that the intended action is possible.

Actual capability resolution, authorization, execution, and failure handling belong to higher layers.

# Supersession Semantics

supersedes identifies an earlier plan that this plan replaces.

superseded_by identifies a later plan that replaces this plan.

Both references are represented using plan IDs.

Plan does not:

- retrieve the referenced plan;
- verify that the referenced plan exists;
- modify the referenced plan;
- automatically establish bidirectional relationships;
- determine why supersession occurred.

Application-level planning or lifecycle management is responsible for maintaining supersession relationships.

# Outcome Semantics

PlanOutcome represents the lifecycle outcome associated with a Plan.

The domain contract represents the outcome but does not independently perform the transition.

For example:

PENDING

The plan exists but has not reached a terminal outcome.

COMPLETED

The plan lifecycle has been completed successfully.

FAILED

The plan lifecycle ended unsuccessfully.

SUPERSEDED

The plan has been replaced by another plan.

ABORTED

The plan lifecycle was intentionally terminated before completion.

These values describe plan lifecycle state only.

They must not be interpreted as authorization verdicts or capability execution results.

# Immutability

Plan uses frozen Pydantic semantics.

After construction:

- plan_id cannot be reassigned;
- task_id cannot be reassigned;
- created_at cannot be reassigned;
- based_on cannot be reassigned;
- assumptions cannot be reassigned;
- constraints cannot be reassigned;
- validity_conditions cannot be reassigned;
- intended_action cannot be reassigned;
- supersedes cannot be reassigned;
- superseded_by cannot be reassigned;
- outcome cannot be reassigned.

Collection fields use tuples rather than mutable lists.

A changed plan must be represented by constructing a new Plan.

# Planning Boundary

Plan represents the result of reasoning.

The planning/application layer is responsible for:

- gathering information required for planning;
- constructing a plan;
- deciding which information is relevant;
- generating assumptions;
- generating constraints;
- generating validity conditions;
- determining intended actions;
- determining whether a new plan supersedes an older plan;
- evaluating whether a plan remains applicable;
- requesting authorization;
- deciding whether a plan should execute.

Plan itself only represents the resulting contract.

# World State Boundary

Plan does not depend on World State.

It does not:

- import domain.worldstate;
- retrieve entities;
- inspect current state;
- reconcile state;
- update state;
- infer state;
- determine whether the world has changed.

A plan may contain IDs or primitive references in based_on, but those references are not resolved by Plan.

# Capability Boundary

Plan does not depend on capability objects.

It does not:

- import domain.capability;
- resolve capabilities;
- authorize capabilities;
- execute capabilities;
- determine capability availability;
- determine capability registration status.

The intended action is descriptive plan data.

The application and authorization layers determine how or whether that intended action may be fulfilled.

# Task Boundary

Plan does not depend on Task objects.

task_id is represented as a string identifier.

Plan does not:

- retrieve the Task;
- modify the Task;
- determine Task lifecycle;
- execute the Task;
- infer Task scope.

Task lifecycle and execution belong to the appropriate higher-level layers.

# Authorization Boundary

Plan does not authorize itself.

It does not:

- produce authorization verdicts;
- inspect grants;
- inspect delegations;
- request approval;
- consume nonces;
- determine whether execution is permitted.

Authorization is performed by the authorization layer using the appropriate contracts.

# Execution Boundary

Plan is not an execution object.

The execution layer is responsible for:

- resolving the intended action;
- resolving required capabilities;
- performing authorization;
- checking current state;
- executing the action;
- handling execution failures;
- recording execution results.

Plan only records the intended structure of the reasoning result.

# Domain and Application Boundary

# Domain owns

- Plan representation
- PlanOutcome representation
- Structural validation
- Immutable plan contracts
- Plan identifiers
- Task identifiers
- Plan references
- Assumptions as data
- Constraints as data
- Validity conditions as data
- Intended action as data
- Plan lifecycle outcome representation

# Application owns

- Creating plans
- Gathering information for planning
- Evaluating whether plans remain valid
- Comparing plans
- Managing supersession
- Deciding whether a plan should execute
- Coordinating authorization
- Coordinating execution
- Updating plan lifecycle state
- Persisting plans through infrastructure

# Authorization owns

- Authorization decisions
- Grant evaluation
- Delegation evaluation
- Approval workflows
- Capability authorization

# Infrastructure owns

- Plan persistence
- Repository implementations
- Database access
- Redis access
- External system access

# Interface owns

- Receiving requests that result in planning
- Presenting plans
- Translating external input into application requests
- Presenting plan outcomes

# What Plan Does NOT Own

domain/plan.py explicitly does NOT own:

- Plan execution
- Capability execution
- Authorization
- Approval workflows
- Current-state retrieval
- World-state reconciliation
- External system access
- Repository access
- Persistence
- Task execution
- Task mutation
- Capability resolution
- Runtime validity evaluation
- LLM execution
- External API calls
- Global mutable state

# Required Tests

The implementation must include tests covering at least:

test_plan_is_structurally_valid()

test_plan_is_frozen()

test_plan_outcome_has_expected_values()

test_plan_uses_immutable_tuples()

test_task_reference_is_stored_as_id()

test_plan_references_are_stored_as_ids()

test_plan_does_not_execute_actions()

test_plan_does_not_resolve_runtime_objects()

test_no_forbidden_layer_imports()

test_no_relative_imports()

# Import Boundary Tests

Tests must statically inspect domain/plan.py and verify that it does not import:

- application
- infrastructure
- interface
- domain.capability
- domain.task
- domain.worldstate
- domain.authorization
- domain.policy
- domain.risk
- runtime services
- repositories
- registries

Only standard-library dependencies and approved Pydantic imports are permitted.

No relative imports are permitted.

# Implementation Notes

1. Keep the implementation intentionally small.

2. Do not add helper methods unless required by this specification.

3. Do not add execution logic.

4. Do not add authorization logic.

5. Do not add runtime state lookup.

6. Do not add repository access.

7. Do not import other Zenith domain modules.

8. Do not introduce connector-specific behavior.

9. Do not use an LLM inside the domain model.

10. Do not add automatic plan mutation or lifecycle transitions.

11. Do not add hidden global state.

12. Preserve immutable tuple semantics for collection fields.

13. Use IDs instead of importing cross-contract domain objects.

14. Structural validation must remain deterministic and side-effect free.

# Public Interface

The module exposes:

- Plan
- PlanOutcome