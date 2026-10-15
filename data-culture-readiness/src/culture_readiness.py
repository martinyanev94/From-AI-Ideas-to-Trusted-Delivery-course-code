from dataclasses import dataclass
from datetime import date
from typing import Iterable


@dataclass(frozen=True)
class ReadinessGap:
    dimension: str
    score: int
    impact: int
    feasibility: int
    action: str
    owner: str
    evidence: str
    review_date: date

    def __post_init__(self) -> None:
        if not 1 <= self.score <= 5:
            raise ValueError("score must be between 1 and 5")
        if not 1 <= self.impact <= 5:
            raise ValueError("impact must be between 1 and 5")
        if not 1 <= self.feasibility <= 5:
            raise ValueError("feasibility must be between 1 and 5")
        for field_name in ("dimension", "action", "owner", "evidence"):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} cannot be empty")


def prioritize_gaps(gaps: Iterable[ReadinessGap]) -> list[ReadinessGap]:
    """Put the weakest readiness gaps first, with impact and feasibility as tie-breakers."""
    return sorted(gaps, key=lambda gap: (gap.score, -gap.impact, -gap.feasibility))


def readiness_plan(gaps: Iterable[ReadinessGap]) -> list[dict[str, str | int]]:
    return [
        {
            "priority": index,
            "dimension": gap.dimension,
            "action": gap.action,
            "owner": gap.owner,
            "evidence": gap.evidence,
            "review_date": gap.review_date.isoformat(),
        }
        for index, gap in enumerate(prioritize_gaps(gaps), start=1)
    ]
