from pydantic import BaseModel, ConfigDict


class DomainScope(BaseModel):
    model_config = ConfigDict(frozen=True)

    allowed_entity_types: tuple[str, ...] = ()
    allowed_domains: tuple[str, ...] = ()
    boundaries: tuple[str, ...] = ()
