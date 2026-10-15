from dataclasses import dataclass
from typing import Literal

Approach = Literal["predictive", "optimization", "hybrid"]


@dataclass(frozen=True)
class ApproachResult:
    approach: Approach
    fit: str
    explainability: str
    feasible: bool
    on_time_rate: float
    total_late_minutes: int
    notes: str = ""

    def __post_init__(self) -> None:
        if not 0 <= self.on_time_rate <= 1:
            raise ValueError("on_time_rate must be between 0 and 1")
        if self.total_late_minutes < 0:
            raise ValueError("total_late_minutes cannot be negative")


def compare(results: list[ApproachResult]) -> ApproachResult:
    """Require a usable method before ranking operational outcomes."""
    if not results:
        raise ValueError("at least one approach is required")
    eligible = [
        result for result in results
        if result.feasible
        and result.fit == "high"
        and result.explainability == "high"
    ]
    if not eligible:
        raise ValueError("no approach meets the decision requirements")
    return max(
        eligible,
        key=lambda result: (
            result.on_time_rate,
            -result.total_late_minutes,
        ),
    )


def example_results() -> list[ApproachResult]:
    return [
        ApproachResult(
            "predictive", "partial", "medium", False, 1.0, 0,
            "risk estimate did not enforce assignment or overlap rules",
        ),
        ApproachResult(
            "optimization", "high", "high", True, 2 / 3, 60,
            "order A, C, B; completions 09:30, 10:00, 10:30",
        ),
    ]


if __name__ == "__main__":
    winner = compare(example_results())
    print(winner.approach)
    print(winner.notes)
