from dataclasses import dataclass, field

VALID_STATUSES = {"pass", "review", "fail"}
REQUIRED_DIMENSIONS = {
    "context",
    "affected_people",
    "fairness",
    "accuracy",
    "fitness_for_purpose",
    "accountability",
}


@dataclass(frozen=True)
class ImpactCheck:
    dimension: str
    status: str
    rationale: str
    owner: str


@dataclass
class ImpactAssessment:
    use_case: str
    context: str
    affected_people: list[str] = field(default_factory=list)
    checks: list[ImpactCheck] = field(default_factory=list)

    def add_check(self, check: ImpactCheck) -> None:
        if check.dimension not in REQUIRED_DIMENSIONS:
            raise ValueError(f"unknown dimension: {check.dimension}")
        if check.status not in VALID_STATUSES:
            raise ValueError(f"invalid status: {check.status}")
        if not check.rationale.strip() or not check.owner.strip():
            raise ValueError("rationale and owner are required")
        self.checks.append(check)


def build_report(assessment: ImpactAssessment) -> dict:
    found = [check.dimension for check in assessment.checks]
    missing = REQUIRED_DIMENSIONS - set(found)
    duplicates = {dimension for dimension in found if found.count(dimension) > 1}
    if missing or duplicates:
        raise ValueError(
            f"missing={sorted(missing)}, duplicates={sorted(duplicates)}"
        )

    return {
        "use_case": assessment.use_case,
        "context": assessment.context,
        "affected_people": assessment.affected_people,
        "checks": [check.__dict__ for check in assessment.checks],
    }
