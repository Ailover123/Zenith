# Module Specification — `domain/scope.py`

## Owns

- `DomainScope`

## Must NOT depend on

- Application
- Infrastructure
- Interface
- World State repositories

## Authority Boundary

Represents the declared domain boundary of a Task.

It may validate scope structure.

It must NOT:
- expand scope;
- retrieve entities;
- authorize expansion;
- infer scope from events;
- access external systems.

## Contract

A scope contains explicit allowed entity types/domains and any declared boundaries required by the task.

## Invariants

1. Scope is explicit and structured.
2. Reasoning cannot directly modify scope.
3. Scope expansion requires an application-level policy-gated request.
4. Domain scope validation performs no I/O.

## Contract Version

```text
DomainScope v1