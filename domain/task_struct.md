# domain/task.py

## Module Ownership

This module owns the pure domain representation of task lifecycle state and task dormancy/resume configuration:

- `Task`
- `TaskEvent`
- `ResumeTrigger`
- `TaskStatus`

## Allowed Dependencies

- Python standard-library types (`datetime`, `enum.Enum`, `re`)
- Pydantic (`BaseModel`, `ConfigDict`, `Field`, `field_validator`)
- `domain.scope.DomainScope`

## Forbidden Dependencies

- application/*
- infrastructure/*
- interface/*
- domain.capability, domain.authorization, domain.policy, domain.risk, domain.worldstate, domain.event, domain.plan

## Public Contracts

### `TaskStatus`
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

### `ResumeTrigger`
- trigger_type: str (snake_case identifier)
- configuration: dict[str, object]

### `TaskEvent`
- event_id: str
- task_id: str
- event_type: str (snake_case identifier)
- timestamp: datetime
- details: dict[str, object]

### `Task`
- task_id: str
- scope: DomainScope
- status: TaskStatus
- created_at: datetime
- parent_task_id: str | None
- plan_id: str | None
- capability_id: str | None
- resume_trigger: ResumeTrigger | None
