from enum import Enum

from pydantic import BaseModel, ConfigDict, model_validator

from domain.vocabulary import Interface, Operation


class PolicyStatus(str, Enum):
    DISCOVERED = "discovered"
    EXTRACTED = "extracted"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    ACTIVE = "active"
    REVOKED = "revoked"


class PolicyVerdict(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_REVIEW = "require_review"
    PROHIBITED = "prohibited"


class Policy(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    platform: str
    operation: Operation
    interface: Interface
    verdict: PolicyVerdict
    status: PolicyStatus
    version: int
    reviewed_by_human: bool

    @model_validator(mode="after")
    def validate_structural_invariants(self) -> "Policy":
        if self.verdict is PolicyVerdict.PROHIBITED and self.status is PolicyStatus.ACTIVE:
            raise ValueError("PROHIBITED policies cannot be ACTIVE")

        if self.status is PolicyStatus.ACTIVE and not self.reviewed_by_human:
            raise ValueError("ACTIVE policies require human review")

        if self.status is PolicyStatus.APPROVED and not self.reviewed_by_human:
            raise ValueError("APPROVED policies require human review")

        return self
