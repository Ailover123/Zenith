from enum import Enum

from pydantic import BaseModel, ConfigDict


class Verdict(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_APPROVAL = "require_approval"
    SECURITY_UNAVAILABLE = "security_unavailable"
    THROTTLED = "throttled"


class DelegationScope(BaseModel):
    model_config = ConfigDict(frozen=True)

    capability_ids: tuple[str, ...] = ()
    subject_ids: tuple[str, ...] = ()


class DecisionObject(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    subject_id: str
    capability_id: str
    verdict: Verdict
    reason: str


class RootGrant(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    subject_id: str
    capability_id: str
    scope: DelegationScope | None = None
