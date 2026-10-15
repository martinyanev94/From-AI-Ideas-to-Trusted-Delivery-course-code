from dataclasses import dataclass
from typing import Literal

Decision = Literal["proceed", "revise", "stop"]


@dataclass
class Brief:
    context: str
    evidence: str
    limitations: str
    decision: Decision
    action: str

    def validate(self) -> None:
        if self.decision not in {"proceed", "revise", "stop"}:
            raise ValueError("decision must be proceed, revise, or stop")
        fields = {
            "context": self.context,
            "evidence": self.evidence,
            "limitations": self.limitations,
            "action": self.action,
        }
        missing = [name for name, value in fields.items() if not value.strip()]
        if missing:
            raise ValueError(f"Missing brief fields: {', '.join(missing)}")

    def render(self) -> str:
        self.validate()
        return "\n".join(
            [
                "# Decision brief",
                f"## Context\n{self.context}",
                f"## Evidence\n{self.evidence}",
                f"## Limitations\n{self.limitations}",
                f"## Decision\n{self.decision}",
                f"## Recommended action\n{self.action}",
            ]
        )
