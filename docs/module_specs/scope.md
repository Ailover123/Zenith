# Module Specification — domain/scope.py

# Status

READY FOR IMPLEMENTATION

# Version

1.0

# Tier

0

# Owns

This module owns the pure domain representation of the declared scope of a Task:

- DomainScope

The module represents what domain/entity boundaries a Task is explicitly permitted to operate within.

It does not perform authorization or scope expansion.

# Must NOT depend on

- application/*
- infrastructure/*
- interface/*
- domain/worldstate.py
- World State repositories
- registries
- repositories
- databases
- Redis
- network clients
- external APIs
- filesystem interfaces

No I/O.

No external state retrieval.

No relative imports.

# Allowed Dependencies

Allowed dependencies are limited to:

- Python standard library types
- Pydantic for the immutable domain contract

DomainScope must remain independently representable.

It must not depend on runtime world-state objects or repositories.

# Authority Boundary

The domain scope module MAY:

- Represent an explicitly declared domain boundary.
- Represent allowed entity types.
- Represent allowed domains.
- Represent declared scope boundaries required by a Task.
- Validate structural consistency of the supplied scope.
- Preserve scope immutably.

The domain scope module MUST NOT:

- Expand scope.
- Infer scope from events.
- Retrieve entities.
- Query World State.
- Query repositories or registries.
- Authorize scope expansion.
- Decide whether scope expansion should be approved.
- Modify an existing scope.
- Access external systems.
- Perform I/O.

Scope expansion is an application-level, policy-gated operation.

# Contract Version

DomainScope v1

# DomainScope

DomainScope represents the explicit domain boundary within which a Task is declared to operate.

The scope must be explicit and structured.

It must contain the declared allowed entity types/domains and any declared boundaries required by the Task.

Cross-contract or external entity references must be represented using IDs or primitive immutable values rather than retrieved runtime objects.

# Public Contract

DomainScope is an immutable/frozen Pydantic model.

The contract contains:

- allowed_entity_types: tuple[str, ...]
- allowed_domains: tuple[str, ...]
- boundaries: tuple[str, ...]

All collections are immutable tuples.

All dimensions default to empty tuples.

An empty dimension means that no additional restriction is declared for that particular dimension.

DomainScope does not interpret an empty dimension as permission to discover or retrieve arbitrary external entities.

# Structural Meaning

allowed_entity_types represents the explicitly declared entity types permitted by the scope.

Examples of values may include domain-level entity type identifiers such as:

- user
- device
- document
- service

The module does not maintain or validate a registry of entity types.

allowed_domains represents explicitly declared domain identifiers within which the Task may operate.

The module does not determine whether those domains currently exist.

boundaries represents additional explicitly declared boundary identifiers required by the Task.

The module does not infer or expand these boundaries.

# Structural Validation

DomainScope validation is limited to structural consistency.

The module MAY reject structurally invalid values required by the contract.

The module MUST NOT validate whether an entity type, domain, or boundary actually exists outside the supplied object.

The module MUST NOT retrieve information to perform validation.

The module MUST NOT infer missing scope information.

# Immutability

DomainScope must be immutable.

After construction:

- allowed_entity_types cannot be reassigned.
- allowed_domains cannot be reassigned.
- boundaries cannot be reassigned.

The underlying collections must use immutable tuple semantics.

No global mutable scope state is permitted.

# Scope Expansion Boundary

Reasoning or execution logic must not directly modify DomainScope.

A request to expand scope is not performed by this module.

The application layer owns:

- receiving a scope-expansion request;
- determining why expansion is needed;
- applying applicable policy;
- obtaining required authorization or approval;
- constructing the resulting scope;
- deciding whether the expanded scope may be used.

DomainScope only represents the resulting declared scope.

# World State Boundary

DomainScope must not depend on World State.

It must not:

- query World State;
- discover entities;
- resolve entity IDs;
- inspect current entity state;
- infer scope from world-state data;
- infer scope from events.

World State retrieval belongs outside the domain scope contract.

# Event Boundary

DomainScope must not infer or mutate scope based on events.

Events may be interpreted by application-level orchestration, but this module remains a pure representation of explicitly declared scope.

# Input → Processing → Output

Input:

- Explicit scope declaration values.

Processing:

- Construct an immutable DomainScope.
- Validate structural consistency.
- Preserve the explicitly supplied scope.

Output:

- Valid immutable DomainScope.

There is no external lookup, authorization decision, scope expansion, persistence, or I/O.

# Invariants

1. DomainScope is explicit and structured.

2. DomainScope is immutable.

3. Entity types are represented explicitly.

4. Domains are represented explicitly.

5. Additional boundaries are represented explicitly.

6. Collection fields use immutable tuple semantics.

7. Empty dimensions represent no additional restriction for that dimension.

8. Empty dimensions do not authorize external discovery or retrieval.

9. Scope validation performs no I/O.

10. Scope validation does not query World State.

11. Scope validation does not query repositories or registries.

12. Reasoning cannot directly modify scope.

13. Scope expansion requires an application-level policy-gated request.

14. Scope expansion is outside the authority of DomainScope.

15. DomainScope does not perform authorization.

16. DomainScope does not retrieve entities.

17. DomainScope does not infer scope from events.

18. DomainScope contains no global mutable state.

# Domain/Application Boundary

## Domain owns

- DomainScope representation.
- Explicit scope structure.
- Structural validation.
- Immutability.
- Deterministic representation of declared boundaries.

## Application owns

- Retrieving relevant external state.
- Determining which entities or domains are relevant.
- Receiving scope-expansion requests.
- Applying policy to scope expansion.
- Requesting authorization or approval for expansion.
- Constructing a new scope after an approved expansion.
- Deciding when a scope is used.

## Infrastructure owns

- Persistence.
- Repository access.
- World State retrieval.
- External system access.

## Interface owns

- Receiving user or external requests.
- Presenting scope information.
- Translating external input into application requests.

# Forbidden Behavior

The implementation must not contain:

- repository calls;
- registry lookups;
- database access;
- Redis access;
- network access;
- filesystem access;
- World State queries;
- event processing;
- authorization logic;
- policy evaluation;
- scope expansion logic;
- approval workflow;
- global mutable registries;
- runtime entity discovery.

# Public Interface

The module exposes:

- DomainScope

No helper service, registry, resolver, expansion engine, or authorization function is required.

# Implementation Constraints

- Use Pydantic for DomainScope.
- Use frozen/immutable Pydantic model semantics.
- Use tuple[str, ...] for collection fields.
- Do not use nested mutable lists as public contract fields.
- Use primitive or ID-based references.
- No I/O.
- No filesystem access.
- No network access.
- No database access.
- No Redis access.
- No repository access.
- No registry access.
- No World State dependency.
- No event dependency.
- No application imports.
- No infrastructure imports.
- No interface imports.
- No relative imports.
- No global mutable state.
- No metaprogramming.
- Explicit behavior over clever abstractions.

# Required Tests

The following behavior must be tested:

- test_domain_scope_is_structurally_valid()
- test_domain_scope_is_frozen()
- test_domain_scope_defaults_to_empty_dimensions()
- test_domain_scope_accepts_entity_types()
- test_domain_scope_accepts_domains()
- test_domain_scope_accepts_boundaries()
- test_domain_scope_uses_immutable_tuples()
- test_empty_scope_dimensions_do_not_require_external_state()
- test_no_forbidden_layer_imports()
- test_no_relative_imports()

Tests must verify only behavior explicitly required by this specification.

Do not invent authorization behavior or scope-expansion behavior.

# Dependency Boundary Test

The structural dependency test must inspect domain/scope.py using ast.

It must reject imports from:

- application
- infrastructure
- interface
- domain.worldstate

It must reject relative imports.

It must not rely only on runtime import behavior.

# Documentation

Create:

domain/scope_struct.md

The documentation must describe:

- ownership;
- allowed dependencies;
- forbidden dependencies;
- DomainScope;
- public fields;
- input → processing → output;
- structural invariants;
- immutability;
- explicit scope semantics;
- empty-dimension semantics;
- scope-expansion boundary;
- World State boundary;
- event boundary;
- domain/application boundary;
- explicit statement that authorization is outside this module.

# Testing Constraint

Tests must verify the behavior explicitly required by this specification.

Do not invent speculative requirements.

If implementation reveals an ambiguity or missing requirement, STOP and report the issue for specification review.

Do not silently expand the contract.

# Files Permitted

Only these files may be created or modified:

D:\academic\Zenith\domain\scope.py

D:\academic\Zenith\domain\scope_struct.md

D:\academic\Zenith\tests\unit\domain\test_scope.py

Nothing else.

# Verification

After implementation:

1. Run the module tests:

python -m pytest tests\unit\domain\test_scope.py -v

2. Run the complete Tier-0 domain suite:

python -m pytest tests\unit\domain\test_vocabulary.py tests\unit\domain\test_policy.py tests\unit\domain\test_risk.py tests\unit\domain\test_capability.py tests\unit\domain\test_authorization.py tests\unit\domain\test_scope.py -v

3. Inspect git status.

Do not modify unrelated files.

# Failure Handling

If a test fails because of an implementation defect, fix the defect within the three permitted files.

If a failure reveals an ambiguity in this specification, STOP.

Do not guess.

Do not modify other modules to make scope tests pass.

Report the ambiguity instead.

# Final Report

When finished, report:

1. Files created/modified.
2. What was implemented.
3. Test command used.
4. Exact module test result.
5. Exact full Tier-0 suite result.
6. Whether all Tier-0 tests passed.
7. Any deviation from the specification.

Do not claim tests passed unless they were actually executed.

Do not modify install.cmd or any unrelated file.