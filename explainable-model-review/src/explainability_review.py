from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

ReviewDepth = Literal["light", "moderate", "deep"]


@dataclass(frozen=True)
class ExplanationRequirement:
    stakeholder_role: str
    decision_stakes: str
    accountability_need: str
    explanation_type: str
    review_depth: ReviewDepth
    accountable_owner: str = ""
    challenge_action: str = ""
    human_check: str = ""
    escalation_path: str = ""
    correction_action: str = ""
    resolution_state: str = "unresolved"

    def validate(self) -> None:
        required = (
            self.stakeholder_role,
            self.decision_stakes,
            self.explanation_type,
        )
        if any(not value.strip() for value in required):
            raise ValueError("role, stakes, and explanation are required")
        if self.review_depth not in {"light", "moderate", "deep"}:
            raise ValueError("review_depth must be light, moderate, or deep")
        if self.resolution_state not in {"open", "resolved", "unresolved"}:
            raise ValueError("invalid resolution_state")


def build_requirements() -> list[ExplanationRequirement]:
    return [
        ExplanationRequirement(
            "affected_person", "high",
            "understand and challenge the outcome",
            "plain-language reason and relevant factors", "deep",
            "review lead", "submit challenge", "human case review",
            "appeals lead", "correct decision when error is confirmed", "resolved",
        ),
        ExplanationRequirement(
            "case_operator", "high",
            "investigate and escalate an unusual case",
            "case factors, limitations, and review guidance", "moderate",
            "operations lead", "open investigation", "case review",
            "risk lead", "reassess recommendation", "resolved",
        ),
        ExplanationRequirement(
            "auditor", "high",
            "verify consistency and accountability",
            "accessible rationale plus technical trace", "deep",
            "audit owner", "request evidence review", "technical verification",
            "governance lead", "correct or withdraw the recommendation", "resolved",
        ),
    ]


def _contains(text: str, *terms: str) -> bool:
    text = text.lower()
    return all(term in text for term in terms)


def review_requirements(requirements: list[ExplanationRequirement]) -> dict[str, object]:
    gaps: list[str] = []
    for item in requirements:
        item.validate()
        text = item.explanation_type
        if item.stakeholder_role == "affected_person" and (
            not _contains(text, "plain-language") or not item.challenge_action.strip()
        ):
            gaps.append("affected_person: explanation or challenge control is insufficient")
        if item.stakeholder_role == "case_operator" and (
            not _contains(text, "case factors") or not item.challenge_action.strip()
        ):
            gaps.append("case_operator: investigation support is insufficient")
        if item.stakeholder_role == "auditor" and not _contains(text, "accessible", "technical trace"):
            gaps.append("auditor: accessible rationale and technical trace are required")
        controls = (
            item.accountable_owner,
            item.human_check,
            item.escalation_path,
            item.correction_action,
        )
        if item.decision_stakes == "high" and item.review_depth == "light":
            gaps.append(f"{item.stakeholder_role}: review is too shallow")
        if any(not control.strip() for control in controls) or item.resolution_state == "unresolved":
            gaps.append(f"{item.stakeholder_role}: accountability control remains unresolved")
    return {"status": "proceed" if not gaps else "revise", "gaps": gaps}


def render_report(requirements: list[ExplanationRequirement]) -> dict[str, object]:
    review = review_requirements(requirements)
    return {"requirements": [asdict(item) for item in requirements], **review}
