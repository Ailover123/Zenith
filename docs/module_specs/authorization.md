# Module Specification — domain/authorization.py

# Status

READY FOR IMPLEMENTATION

# Version

1.0

# Tier

0

# Owns

This module owns the pure domain representation of authorization decisions and authority scopes.

- Verdict
- DecisionObject
- RootGrant
- DelegationScope

This module represents authorization-related domain contracts.

It does not perform authorization.

# Must NOT depend on

- application/*
- infrastructure/*
- interface/*
- Runtime repositories
- Runtime services
- Registries
- Persistence systems
- Databases
- Redis
- Network clients
- External APIs
- Filesystem interfaces

Use IDs for cross-contract references.

The module must not retrieve or resolve external state.

No I/O.

No relative imports.

# Allowed Dependencies

Allowed dependencies are limited to:

- Python standard-library types and enums
- Pydantic for immutable domain contracts

This module must not depend on:

- domain.capability
- domain.policy
- domain.risk
- Application services
- Infrastructure services
- Interface-layer objects
- Runtime authorization engines

Authorization contracts must remain independently representable.

# Authority Boundary

## MAY

- Represent authorization verdicts.
- Represent authorization decision objects.
- Represent root authority grants.
- Represent delegation scopes.
- Validate structural consistency.
- Validate that required IDs and scope information are structurally present.
- Represent relationships between authority contracts using IDs.
- Represent the immutable result of an authorization evaluation.

## MUST NOT

- Perform authorization itself.
- Query current grants.
- Query registries.
- Resolve identities.
- Resolve capabilities.
- Consume nonces.
- Persist approvals.
- Persist grants.
- Execute capabilities.
- Call external systems.
- Determine runtime registration status.
- Retrieve delegation state.
- Modify grants.
- Modify policies.
- Modify capabilities.
- Decide runtime approval workflows.

The domain owns the shape and structural validity of authorization contracts.

The application and runtime authorization layers own the actual authorization process.

# Verdict

Verdict represents the outcome category of an authorization evaluation.

## Required values

- ALLOW
- DENY
- REQUIRE_APPROVAL
- SECURITY_UNAVAILABLE
- THROTTLED

No additional verdict values may be introduced without a specification change.

## ALLOW

The authorization evaluation permits the requested action.

## DENY

The authorization evaluation rejects the requested action.

## REQUIRE_APPROVAL

The action cannot proceed without an approval process handled outside this domain module.

The domain contract represents this result only.

It does not execute the approval workflow.

## SECURITY_UNAVAILABLE

The authorization or security system cannot safely establish an authorization result.

This is not equivalent to ALLOW.

The domain only represents this result.

The runtime authorization layer determines when this verdict should be emitted.

## THROTTLED

The request is structurally recognized but cannot currently proceed because a runtime security, rate, or resource constraint requires throttling.

The domain contract only represents this result.

It does not perform throttling.

# DecisionObject

DecisionObject represents the immutable result of an authorization evaluation.

It must contain enough information to represent:

- The decision identity
- The subject or actor associated with the decision
- The requested capability
- The resulting verdict
- The reason for the decision

Cross-contract references must use IDs.

The decision object must not contain live service or repository objects.

## Required fields

- id: str
- subject_id: str
- capability_id: str
- verdict: Verdict
- reason: str

DecisionObject is a frozen Pydantic model.

The decision object represents a result.

It does not itself evaluate whether the subject is authorized.

# RootGrant

RootGrant represents a root authority grant from which authority may originate.

It is a pure immutable domain contract.

## Required fields

- id: str
- subject_id: str
- capability_id: str

## Optional scope

A RootGrant may carry:

- scope: DelegationScope

if the grant carries explicit delegation constraints.

RootGrant must use IDs rather than nested runtime objects.

RootGrant does not verify:

- Whether the subject currently exists
- Whether the capability currently exists
- Whether the grant is currently registered
- Whether the grant has been revoked elsewhere
- Whether the subject is currently authorized

Those are runtime or application concerns.

# DelegationScope

DelegationScope represents the structural boundaries within which authority may be delegated.

The scope is represented using IDs and immutable collections.

## Required fields

- capability_ids: tuple[str, ...]
- subject_ids: tuple[str, ...]

Both collections default to empty tuples.

An empty collection means that dimension imposes no additional structural restriction.

The scope must remain a pure data contract.

It must not query whether referenced subjects or capabilities exist.

It must not determine runtime authorization.

# Structural Validation

The authorization module performs only structural validation.

At minimum:

- IDs must be structurally valid non-empty strings.
- DecisionObject must contain a valid Verdict.
- DecisionObject must contain a required subject identifier.
- DecisionObject must contain a required capability identifier.
- DecisionObject must contain a decision reason.
- RootGrant must contain required authority identifiers.
- DelegationScope must contain immutable ID collections.
- Cross-contract references must remain ID-based.
- Authorization contracts must be immutable.

Invalid structural state must fail explicitly during construction.

# Immutability

All authorization domain contracts must use frozen or immutable Pydantic semantics.

The following must be immutable:

- DecisionObject
- RootGrant
- DelegationScope

Verdict is an enum and is inherently immutable.

No contract may expose mutable global state.

# Domain and Application Boundary

## Domain owns

- Verdict vocabulary
- Authorization decision representation
- Root-grant representation
- Delegation-scope representation
- Structural validation
- Immutable authorization contracts
- ID-based cross-contract references

## Application owns

- Retrieving grants
- Retrieving delegation information
- Determining which authority records are relevant
- Supplying authorization inputs
- Orchestrating authorization evaluation
- Approval workflow orchestration
- Nonce lifecycle
- Runtime throttling
- Runtime registration checks

## Authorization Runtime owns

- Evaluating whether a subject is authorized
- Evaluating grants
- Evaluating delegation
- Evaluating scope against a request
- Producing the appropriate DecisionObject
- Enforcing authorization decisions

domain/authorization.py must never become an authorization engine.

# Security Boundary

SECURITY_UNAVAILABLE is intentionally represented as a distinct verdict.

The system must never treat inability to establish security state as equivalent to permission.

However, this module only represents the verdict.

It does not decide when the verdict should be emitted.

The runtime authorization or application layer determines when security state is unavailable.

# Approval Boundary

REQUIRE_APPROVAL represents a decision requiring approval.

The domain contract does not:

- Create an approval request
- Persist an approval
- Notify a human
- Wait for approval
- Consume approval tokens
- Execute the capability

Those behaviors belong outside this module.

# Throttling Boundary

THROTTLED represents a decision in which execution cannot proceed because the relevant runtime security, resource, or rate constraint requires throttling.

This module does not:

- Maintain counters
- Consume tokens
- Track rate limits
- Access Redis
- Access databases
- Enforce throttling

It only represents the resulting verdict.

# Cross-Contract References

Cross-contract relationships must be represented using IDs.

Examples:

- DecisionObject.capability_id
- DecisionObject.subject_id
- RootGrant.subject_id
- RootGrant.capability_id
- DelegationScope.capability_ids
- DelegationScope.subject_ids

Do not embed:

- Capability
- Policy
- Risk
- User
- Repository
- Service
- AuthorizationEngine

objects inside authorization contracts.

This prevents the domain authorization module from coupling itself to runtime systems.

# Invariants

1. Verdict contains exactly ALLOW, DENY, REQUIRE_APPROVAL, SECURITY_UNAVAILABLE, and THROTTLED.
2. DecisionObject is immutable.
3. RootGrant is immutable.
4. DelegationScope is immutable.
5. Required IDs must be structurally present.
6. Cross-contract references use IDs.
7. Empty delegation-scope dimensions impose no additional structural restriction.
8. DecisionObject represents an authorization result but does not perform authorization.
9. RootGrant represents authority but does not verify runtime registration.
10. DelegationScope represents authority boundaries but does not evaluate runtime authorization.
11. SECURITY_UNAVAILABLE remains distinct from ALLOW.
12. REQUIRE_APPROVAL does not execute an approval workflow.
13. THROTTLED does not perform throttling.
14. The module performs no I/O.
15. The module performs no authorization evaluation.
16. The module does not query registries or repositories.
17. The module does not consume nonces.
18. The module does not persist state.
19. The module does not execute capabilities.
20. The module contains no global mutable state.
21. The module has no application, infrastructure, or interface dependencies.

# Required Tests

## Verdict vocabulary

- test_verdict_has_expected_values

Verdict must contain exactly:

- ALLOW
- DENY
- REQUIRE_APPROVAL
- SECURITY_UNAVAILABLE
- THROTTLED

## DecisionObject

- test_decision_object_is_structurally_valid
- test_decision_object_is_frozen
- test_decision_object_requires_subject_id
- test_decision_object_requires_capability_id
- test_decision_object_requires_reason

## RootGrant

- test_root_grant_is_structurally_valid
- test_root_grant_is_frozen
- test_root_grant_requires_subject_id
- test_root_grant_requires_capability_id

## DelegationScope

- test_delegation_scope_is_structurally_valid
- test_delegation_scope_defaults_to_unrestricted_dimensions
- test_delegation_scope_is_frozen
- test_delegation_scope_accepts_capability_ids
- test_delegation_scope_accepts_subject_ids

## Verdict representation

- test_allow_verdict_is_representable
- test_deny_verdict_is_representable
- test_require_approval_verdict_is_representable
- test_security_unavailable_verdict_is_representable
- test_throttled_verdict_is_representable

## Dependency boundary

- test_no_forbidden_layer_imports

The static import test must reject imports from:

- application
- infrastructure
- interface

It must also reject relative imports.

The test must inspect source using ast rather than relying only on runtime import behavior.

# Testing Constraint

Tests must verify only behavior explicitly required by this specification.

Do not invent:

- Runtime authorization algorithms
- Grant expiration logic
- Nonce semantics
- Approval persistence
- Rate-limiting algorithms
- Identity resolution
- Capability lookup
- Policy evaluation
- Risk evaluation

If implementation reveals an ambiguity or missing requirement, stop and return the issue for specification review rather than silently expanding scope.

# Documentation

Create:

domain/authorization_struct.md

The documentation must describe:

- Module ownership
- Allowed dependencies
- Forbidden dependencies
- Input to processing to output
- Verdict
- DecisionObject
- RootGrant
- DelegationScope
- Structural invariants
- Immutability
- ID-based references
- Domain/application boundary
- Security-unavailable boundary
- Approval boundary
- Throttling boundary
- The fact that runtime authorization is outside this module

# Public Interface

The module exposes exactly:

- Verdict
- DecisionObject
- RootGrant
- DelegationScope

No authorization engine or runtime authorization function belongs in this module.

# Implementation Constraints

- Use Pydantic for domain contracts.
- Use Enum for Verdict.
- Use immutable or frozen contract semantics.
- Use IDs for cross-contract references.
- Use tuples for immutable ID collections.
- No I/O.
- No filesystem access.
- No network access.
- No database access.
- No Redis access.
- No repository access.
- No registry access.
- No runtime service access.
- No application imports.
- No infrastructure imports.
- No interface imports.
- No relative imports.
- No global mutable state.
- No metaprogramming.
- No authorization execution logic.
- No approval workflow logic.
- No throttling implementation.
- No nonce lifecycle logic.
- Explicit behavior over clever abstractions.

# Files Permitted

AGY may create or modify only:

D:\academic\Zenith\domain\authorization.py

D:\academic\Zenith\domain\authorization_struct.md

D:\academic\Zenith\tests\unit\domain\test_authorization.py

Nothing else.

If anything in this specification is ambiguous, stop and ask rather than guessing.