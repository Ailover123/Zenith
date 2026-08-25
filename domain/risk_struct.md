# domain/risk.py

## Ownership

This module owns pure risk representation and deterministic effective-risk resolution:

- `Risk`
- `RiskMode`
- `RiskLevel`
- `effective_risk_level()`

## Allowed Dependencies

Allowed dependencies are Python standard library enum/type support and Pydantic for the immutable `Risk` contract.

This module must not import `application`, `infrastructure`, `interface`, `domain.capability`, `domain.policy`, or `domain.authorization`.

## Input -> Processing -> Output

`effective_risk_level()` receives a `Risk` and an explicit `dict[str, Risk]` containing related risks. It resolves the effective level deterministically from those supplied objects and returns a `RiskLevel`.

The resolver does not retrieve risks, access registries, perform I/O, or inspect external state.

## Public Contracts

`RiskLevel` values:

- `LOW`
- `MEDIUM`
- `HIGH`
- `CRITICAL`

`RiskMode` values:

- `EXPLICIT`
- `INHERITED`
- `AGGREGATE`

`Risk` fields:

- `id: str`
- `level: RiskLevel`
- `mode: RiskMode`
- `source_risk_id: str | None`
- `child_risk_ids: tuple[str, ...]`

`Risk` is a frozen Pydantic model.

## Structural Invariants

- `INHERITED` risks require a source risk ID.
- `AGGREGATE` risks require one or more child risk IDs.
- References are IDs, not nested `Risk` objects.
- Risk contracts are immutable.

## Domain/Application Boundary

The domain layer owns risk representation, structural validation, risk ordering, deterministic resolution, unknown-reference handling, and cycle detection.

The application layer owns retrieving risks, deciding which risks are relevant, supplying `related_risks`, deciding when resolution occurs, and integrating risk with policy, authorization, approvals, or execution.

## Effective-Risk Resolution

- `EXPLICIT` resolves to its declared level.
- `INHERITED` resolves recursively through `source_risk_id`.
- `AGGREGATE` resolves all `child_risk_ids` and returns the maximum effective level using `LOW < MEDIUM < HIGH < CRITICAL`.

## Unknown References

Unknown inherited or aggregate references resolve conservatively to `CRITICAL`. The resolver never fetches missing risks.

## Cycle Detection

Cycles are detected with a deterministic visited set and fail explicitly with an exception. Cycles are not treated as unknown references.
