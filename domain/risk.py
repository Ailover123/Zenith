from enum import Enum
from typing import Self

from pydantic import BaseModel, ConfigDict, model_validator


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskMode(str, Enum):
    EXPLICIT = "explicit"
    INHERITED = "inherited"
    AGGREGATE = "aggregate"


class Risk(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    level: RiskLevel
    mode: RiskMode
    source_risk_id: str | None = None
    child_risk_ids: tuple[str, ...] = ()

    @model_validator(mode="after")
    def validate_structural_consistency(self) -> Self:
        if self.mode is RiskMode.INHERITED and self.source_risk_id is None:
            raise ValueError("INHERITED risks require a source risk reference")

        if self.mode is RiskMode.AGGREGATE and len(self.child_risk_ids) == 0:
            raise ValueError("AGGREGATE risks require child risk references")

        return self


def effective_risk_level(
    risk: Risk,
    related_risks: dict[str, Risk],
) -> RiskLevel:
    risk_level_order = {
        RiskLevel.LOW: 1,
        RiskLevel.MEDIUM: 2,
        RiskLevel.HIGH: 3,
        RiskLevel.CRITICAL: 4,
    }

    def resolve(current_risk: Risk, visited_risk_ids: set[str]) -> RiskLevel:
        if current_risk.id in visited_risk_ids:
            raise ValueError("risk cycle detected")

        if current_risk.mode is RiskMode.EXPLICIT:
            return current_risk.level

        next_visited_risk_ids = visited_risk_ids | {current_risk.id}

        if current_risk.mode is RiskMode.INHERITED:
            source_risk = related_risks.get(current_risk.source_risk_id or "")
            if source_risk is None:
                return RiskLevel.CRITICAL

            return resolve(source_risk, next_visited_risk_ids)

        child_levels: list[RiskLevel] = []
        for child_risk_id in current_risk.child_risk_ids:
            child_risk = related_risks.get(child_risk_id)
            if child_risk is None:
                return RiskLevel.CRITICAL

            child_levels.append(resolve(child_risk, next_visited_risk_ids))

        return max(child_levels, key=lambda risk_level: risk_level_order[risk_level])

    return resolve(risk, set())
