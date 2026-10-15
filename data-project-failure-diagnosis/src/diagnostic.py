from dataclasses import dataclass
from typing import List


CATEGORIES = {"goal", "people", "data", "expectation", "delivery"}


@dataclass(frozen=True)
class RecoveryAction:
    root_cause: str
    intervention: str
    owner: str
    evidence: List[str]
    outcome_metric: str
    leading_indicator: str
    guardrail: str
    decision_rule: str

    def validate(self) -> List[str]:
        errors = []
        for name in ("root_cause", "intervention", "owner", "outcome_metric", "leading_indicator", "guardrail", "decision_rule"):
            if not getattr(self, name).strip():
                errors.append(f"{name} is required")
        if len(self.evidence) < 2:
            errors.append("at least two evidence items are required")
        return errors


def recovery_status(action: RecoveryAction, outcome_improved: bool, guardrail_holds: bool) -> str:
    if action.validate():
        return "invalid"
    if outcome_improved and guardrail_holds:
        return "proceed"
    return "revise"


def build_example() -> RecoveryAction:
    return RecoveryAction(
        root_cause="No accountable sponsor or agreed business outcome",
        intervention="Appoint a sponsor and reframe the decision with operations",
        owner="Business sponsor",
        evidence=[
            "No named owner can approve scope",
            "Operations was not included in the decision definition",
            "Technical score is being used as the success proxy",
        ],
        outcome_metric="Median decision turnaround time",
        leading_indicator="Approved decision brief used in weekly reviews",
        guardrail="No increase in incorrect escalations",
        decision_rule="Proceed only if outcome improves and guardrail holds",
    )
