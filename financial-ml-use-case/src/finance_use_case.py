from dataclasses import dataclass
from enum import Enum
from typing import Tuple


class RiskTolerance(str, Enum):
    CAUTIOUS = "cautious"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"


@dataclass(frozen=True)
class FinanceUseCase:
    name: str
    intended_decision: str
    decision_owner: str
    risk_tolerance: RiskTolerance
    explanation_needs: Tuple[str, ...]
    evidence_requirements: Tuple[str, ...]

    def validate(self) -> list[str]:
        errors: list[str] = []
        required = {
            "name": self.name,
            "intended_decision": self.intended_decision,
            "decision_owner": self.decision_owner,
        }
        errors.extend(
            field for field, value in required.items() if not value.strip()
        )
        if self.risk_tolerance == RiskTolerance.CAUTIOUS:
            if not self.explanation_needs:
                errors.append("cautious use cases need explanation needs")
            if not self.evidence_requirements:
                errors.append("cautious use cases need evidence requirements")
        return errors


@dataclass(frozen=True)
class EvidenceClaim:
    statement: str
    evidence_status: str


@dataclass(frozen=True)
class RiskRegisterEntry:
    risk: str
    consequence: str
    control: str
    accountable_owner: str
    review_trigger: str

    def validate(self) -> list[str]:
        required = {
            "risk": self.risk,
            "consequence": self.consequence,
            "control": self.control,
            "accountable_owner": self.accountable_owner,
            "review_trigger": self.review_trigger,
        }
        return [
            field for field, value in required.items() if not value.strip()
        ]


ALLOWED_STATUSES = {"supported", "partial", "unsupported"}


def recommendation(
    use_case: FinanceUseCase,
    claims: Tuple[EvidenceClaim, ...],
    risk: RiskRegisterEntry,
) -> str:
    if use_case.validate() or risk.validate() or not claims:
        return "revise"
    if any(
        not claim.statement.strip()
        or claim.evidence_status not in ALLOWED_STATUSES
        or claim.evidence_status != "supported"
        for claim in claims
    ):
        return "revise"
    return "bounded_pilot"
