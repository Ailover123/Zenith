from datetime import datetime
from enum import Enum
import re

from pydantic import BaseModel, ConfigDict, Field, field_validator

from domain.scope import DomainScope


class TaskStatus(str, Enum):
    CREATED = "created"
    OBSERVING = "observing"
    PLANNING = "planning"
    REVALIDATING = "revalidating"
    ACTING = "acting"
    WAITING = "waiting"
    DELEGATED = "delegated"
    ASKING = "asking"
    SURFACED = "surfaced"
    COMPLETED = "completed"
    FAILED = "failed"
    ESCALATED_TO_HUMAN = "escalated_to_human"


class ResumeTrigger(BaseModel):
    model_config = ConfigDict(frozen=True)

    trigger_type: str
    configuration: dict[str, object] = Field(default_factory=dict)

    @field_validator("trigger_type")
    @classmethod
    def validate_trigger_type(cls, v: str) -> str:
        if not re.match(r"^[a-z][a-z0-9_]*$", v):
            raise ValueError(
                f"trigger_type must be a non-empty snake_case identifier, got '{v}'"
            )
        return v


class TaskEvent(BaseModel):
    model_config = ConfigDict(frozen=True)

    event_id: str
    task_id: str
    event_type: str
    timestamp: datetime
    details: dict[str, object] = Field(default_factory=dict)

    @field_validator("event_type")
    @classmethod
    def validate_event_type(cls, v: str) -> str:
        if not re.match(r"^[a-z][a-z0-9_]*$", v):
            raise ValueError(
                f"event_type must be a non-empty snake_case identifier, got '{v}'"
            )
        return v


class Task(BaseModel):
    model_config = ConfigDict(frozen=True)

    task_id: str
    scope: DomainScope = Field(default_factory=DomainScope)
    status: TaskStatus = TaskStatus.CREATED
    created_at: datetime
    parent_task_id: str | None = None
    plan_id: str | None = None
    capability_id: str | None = None
    resume_trigger: ResumeTrigger | None = None
