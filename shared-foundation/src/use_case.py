from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class UseCaseSpecification:
    decision: str
    stakeholder: str
    intended_outcome: str
    success_signal: str
    guardrail_metric: str

    def validate(self) -> List[str]:
        fields = {
            "decision": self.decision,
            "stakeholder": self.stakeholder,
            "intended_outcome": self.intended_outcome,
            "success_signal": self.success_signal,
            "guardrail_metric": self.guardrail_metric,
        }
        return [f"{name} is required" for name, value in fields.items() if not value.strip()]
