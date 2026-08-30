# domain/plan.py

## Module Ownership

This module owns the pure domain representation of a structured reasoning plan:

- `Plan`
- `PlanOutcome`

## Allowed Dependencies

- Python standard-library types (`datetime`, `enum.Enum`)
- Pydantic (`BaseModel`, `ConfigDict`, `Field`)

## Forbidden Dependencies

- application/*
- infrastructure/*
- interface/*
- domain.capability, domain.task, domain.worldstate

## Public Contracts

### `PlanOutcome`
- PENDING = "pending"
- COMPLETED = "completed"
- FAILED = "failed"
- SUPERSEDED = "superseded"
- ABORTED = "aborted"

### `Plan`
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
