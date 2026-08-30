from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class EntityType(str, Enum):
    USER = "user"
    DEVICE = "device"
    SERVICE = "service"
    RESOURCE = "resource"
    DOCUMENT = "document"
    SYSTEM = "system"


class WorldStateEntity(BaseModel):
    model_config = ConfigDict(frozen=True)

    entity_id: str
    entity_type: EntityType
    current_state: dict[str, object]
    state_version: int = Field(ge=0)
    last_updated_event_id: str
