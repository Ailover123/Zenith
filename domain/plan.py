from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class PlanOutcome(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    SUPERSEDED = "superseded"
    ABORTED = "aborted"


class Plan(BaseModel):
    model_config = ConfigDict(frozen=True)

    plan_id: str
    task_id: str
    created_at: datetime
    based_on: tuple[str, ...] = ()
    assumptions: tuple[str, ...] = ()
    constraints: tuple[str, ...] = ()
    validity_conditions: tuple[str, ...] = ()
    intended_action: str
    supersedes: str | None = None
    superseded_by: str | None = None
    outcome: PlanOutcome = PlanOutcome.PENDING
