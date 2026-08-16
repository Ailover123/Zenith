# Module Specification — `domain/task.py`

## Owns

- `Task`
- `TaskEvent`
- `ResumeTrigger`
- `TaskStatus`

## Must NOT depend on

- Infrastructure
- Interface
- Concrete application services

May depend on `domain/scope.py`.

## Authority Boundary

Represents task lifecycle and dormancy/resume configuration.

It may validate structural consistency.

It must NOT:
- execute tasks;
- evaluate triggers against current time/events;
- retrieve World State;
- invoke capabilities;
- persist itself.

## TaskStatus

```text
CREATED
OBSERVING
PLANNING
REVALIDATING
ACTING
WAITING
DELEGATED
ASKING
SURFACED
COMPLETED
FAILED
ESCALATED_TO_HUMAN