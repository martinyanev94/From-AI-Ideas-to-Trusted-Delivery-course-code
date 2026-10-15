from dataclasses import asdict, dataclass
from typing import Iterable

REQUIRED_DIMENSIONS = {"fairness", "accuracy", "fitness", "accountability"}
REQUIRED_REVIEW_STATES = {
    "explained",
    "challenged",
    "resolved",
    "feedback_recorded",
}


@dataclass(frozen=True)
class ImpactItem:
    dimension: str
    finding: str
    rationale: str
    owner: str

    def validate(self) -> None:
        if self.dimension not in REQUIRED_DIMENSIONS:
            raise ValueError(f"unknown dimension: {self.dimension}")
        if not self.finding.strip() or not self.rationale.strip():
            raise ValueError("finding and rationale are required")
        if not self.owner.strip():
            raise ValueError("owner is required")


def validate_items(items: Iterable[ImpactItem]) -> None:
    materialized = list(items)
    for item in materialized:
        item.validate()
    found = {item.dimension for item in materialized}
    missing = REQUIRED_DIMENSIONS - found
    if missing:
        raise ValueError(f"missing dimensions: {sorted(missing)}")


def build_report(
    context: str,
    affected_people: list[str],
    items: list[ImpactItem],
    review_states: list[str],
    unresolved_controls: list[str],
) -> dict:
    if not context.strip() or not affected_people:
        raise ValueError("context and affected people are required")
    validate_items(items)
    missing_states = REQUIRED_REVIEW_STATES - set(review_states)
    status = "proceed" if not missing_states and not unresolved_controls else "revise"
    return {
        "context": context,
        "affected_people": affected_people,
        "status": status,
        "missing_review_states": sorted(missing_states),
        "unresolved_controls": unresolved_controls,
        "items": [asdict(item) for item in items],
    }
