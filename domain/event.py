from datetime import datetime
import re

from pydantic import BaseModel, ConfigDict, field_validator


class ObservationEvent(BaseModel):
    model_config = ConfigDict(frozen=True)

    event_id: str
    source: str
    source_native_id: str
    event_type: str
    timestamp: datetime
    resource_key: str
    raw_payload: object
    normalized_payload: dict[str, object]
    provenance: str
    correlation_id: str

    @field_validator("event_type")
    @classmethod
    def validate_event_type_structure(cls, v: str) -> str:
        if not re.match(r"^[a-z][a-z0-9_]*$", v):
            raise ValueError(
                f"event_type must be a non-empty snake_case identifier, got '{v}'"
            )
        return v
