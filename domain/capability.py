from typing import Self

from pydantic import BaseModel, ConfigDict, model_validator

from domain.policy import Policy, PolicyVerdict
from domain.risk import Risk, RiskLevel, RiskMode
from domain.vocabulary import Interface, Operation


class CapabilityTemplate(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    operation: Operation
    interface: Interface


class ConstraintScope(BaseModel):
    model_config = ConfigDict(frozen=True)

    platforms: tuple[str, ...] = ()
    operations: tuple[Operation, ...] = ()
    interfaces: tuple[Interface, ...] = ()


class Capability(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    template_id: str
    platform: str
    operation: Operation
    interface: Interface
    policy: Policy
    risk: Risk
    scope: ConstraintScope = ConstraintScope()
    requires_approval: bool
    active: bool

    @model_validator(mode="after")
    def validate_structural_invariants(self) -> Self:
        if self.policy.verdict is PolicyVerdict.PROHIBITED and self.active:
            raise ValueError("PROHIBITED policies cannot back an active capability")

        if (
            self.risk.mode is RiskMode.EXPLICIT
            and self.risk.level in (RiskLevel.HIGH, RiskLevel.CRITICAL)
            and not self.requires_approval
        ):
            raise ValueError(
                f"Explicit {self.risk.level.name} risk requires requires_approval=True"
            )

        if (
            self.policy.verdict is PolicyVerdict.REQUIRE_REVIEW
            and not self.requires_approval
        ):
            raise ValueError(
                "REQUIRE_REVIEW policy requires requires_approval=True"
            )

        if len(self.scope.platforms) > 0 and self.platform not in self.scope.platforms:
            raise ValueError(
                f"Platform '{self.platform}' is not within declared platform scope"
            )

        if (
            len(self.scope.operations) > 0
            and self.operation not in self.scope.operations
        ):
            raise ValueError(
                f"Operation '{self.operation}' is not within declared operation scope"
            )

        if (
            len(self.scope.interfaces) > 0
            and self.interface not in self.scope.interfaces
        ):
            raise ValueError(
                f"Interface '{self.interface}' is not within declared interface scope"
            )

        return self
