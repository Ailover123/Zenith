# domain/policy.py

## Ownership

This module owns the pure domain representation of a platform policy and its structural lifecycle state:

- `Policy`
- `PolicyStatus`
- `PolicyVerdict`

## Dependencies

Allowed dependencies are Python standard library support for enum definition, Pydantic for the `Policy` contract model, and `domain.vocabulary` for `Operation` and `Interface`.

It must not depend on `application`, `infrastructure`, `interface`, persistence, discovery mechanisms, network, filesystem, Redis, Postgres, human-review workflows, runtime authorization, or policy registries.

## Contracts

`PolicyStatus` v1 lifecycle states:

- `DISCOVERED`
- `EXTRACTED`
- `PENDING_REVIEW`
- `APPROVED`
- `ACTIVE`
- `REVOKED`

`PolicyVerdict` v1 outcomes:

- `ALLOW`
- `DENY`
- `REQUIRE_REVIEW`
- `PROHIBITED`

`Policy` fields:

- `id: str`
- `platform: str`
- `operation: Operation`
- `interface: Interface`
- `verdict: PolicyVerdict`
- `status: PolicyStatus`
- `version: int`
- `reviewed_by_human: bool`

`Policy` is a frozen Pydantic model that validates structural invariants after model construction.

## Structural Invariants

- A `PROHIBITED` policy must never have `ACTIVE` status.
- An `ACTIVE` policy must have `reviewed_by_human=True`.
- An `APPROVED` policy must have `reviewed_by_human=True`.

## Domain/Application Boundary

The domain validates whether a supplied policy state is structurally valid. The application layer owns when and how lifecycle transitions occur.

This module does not discover, persist, activate, deactivate, authorize, or retrieve external state.

## Public Interface

The public interface exposed by this module is:

- `Policy`
- `PolicyStatus`
- `PolicyVerdict`
