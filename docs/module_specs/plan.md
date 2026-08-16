# Module Specification — `domain/plan.py`

## Owns

- `Plan`
- `PlanOutcome`

## Must NOT depend on

- Application
- Infrastructure
- Interface
- Capability objects
- Task objects

Cross-contract references use IDs.

## Authority Boundary

Represents a structured reasoning plan.

It may validate structural consistency.

It must NOT:
- execute actions;
- retrieve state;
- revalidate state;
- authorize capabilities;
- decide whether a plan should execute.

## Contract

```text
Plan
├── plan_id
├── task_id
├── created_at
├── based_on
├── assumptions
├── constraints
├── validity_conditions
├── intended_action
├── supersedes
├── superseded_by
└── outcome