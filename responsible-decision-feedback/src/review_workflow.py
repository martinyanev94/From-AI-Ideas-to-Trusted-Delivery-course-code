from dataclasses import dataclass, field
from enum import Enum


class InvalidTransition(ValueError):
    pass


class ReviewState(str, Enum):
    DECIDED = "decided"
    EXPLAINED = "explained"
    CHALLENGED = "challenged"
    ESCALATED = "escalated"
    RESOLVED = "resolved"
    FEEDBACK_RECORDED = "feedback_recorded"


@dataclass
class ReviewCase:
    case_id: str
    affected_person: str
    decision: str
    rationale: str
    state: ReviewState = ReviewState.DECIDED
    challenge_reason: str = ""
    outcome: str = ""
    feedback: str = ""

    def explain(self) -> None:
        if self.state is not ReviewState.DECIDED:
            raise InvalidTransition("only decisions can be explained")
        self.state = ReviewState.EXPLAINED

    def challenge(
        self,
        reason: str,
        *,
        material_harm: bool,
        missing_evidence: bool,
    ) -> None:
        if self.state is not ReviewState.EXPLAINED:
            raise InvalidTransition(
                "a person must receive an explanation first"
            )
        if not reason.strip():
            raise ValueError("challenge reason cannot be empty")
        self.challenge_reason = reason
        if material_harm or missing_evidence:
            self.state = ReviewState.ESCALATED
        else:
            self.state = ReviewState.CHALLENGED

    def resolve(self, outcome: str) -> None:
        if self.state not in {
            ReviewState.CHALLENGED,
            ReviewState.ESCALATED,
        }:
            raise InvalidTransition("only challenged cases can be resolved")
        if not outcome.strip():
            raise ValueError("resolution outcome cannot be empty")
        self.outcome = outcome
        self.state = ReviewState.RESOLVED

    def record_feedback(self, feedback: str) -> None:
        if self.state is not ReviewState.RESOLVED:
            raise InvalidTransition(
                "resolve the review before recording feedback"
            )
        if not feedback.strip():
            raise ValueError("feedback cannot be empty")
        self.feedback = feedback
        self.state = ReviewState.FEEDBACK_RECORDED


@dataclass
class FeedbackRegister:
    entries: list[str] = field(default_factory=list)

    def add(self, case: ReviewCase) -> None:
        if case.state is not ReviewState.FEEDBACK_RECORDED:
            raise InvalidTransition("only completed feedback can be registered")
        self.entries.append(case.feedback)
