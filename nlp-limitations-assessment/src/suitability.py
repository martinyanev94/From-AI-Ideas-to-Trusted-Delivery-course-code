from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class NLPProposal:
    name: str
    intended_outcome: str
    input_description: str
    ambiguity_examples: Tuple[str, ...]
    evidence_requirements: Tuple[str, ...]
    risks: Tuple[str, ...]
    non_goals: Tuple[str, ...]
    human_review_required: bool

    def validate(self) -> list[str]:
        fields = {
            "name": self.name,
            "intended_outcome": self.intended_outcome,
            "input_description": self.input_description,
        }
        errors = [name for name, value in fields.items() if not value.strip()]
        collection_fields = {
            "ambiguity_examples": self.ambiguity_examples,
            "evidence_requirements": self.evidence_requirements,
            "risks": self.risks,
            "non_goals": self.non_goals,
        }
        errors.extend(
            name for name, values in collection_fields.items() if not values
        )
        return errors


def assess(proposal: NLPProposal) -> dict[str, object]:
    errors = proposal.validate()
    if errors:
        return {
            "recommendation": "revise",
            "reasons": [f"missing: {field}" for field in errors],
        }

    if not proposal.human_review_required:
        return {
            "recommendation": "revise",
            "reasons": ["define a human review control before adoption"],
        }

    return {
        "recommendation": "proceed to bounded evaluation",
        "reasons": [
            "outcome, ambiguity, evidence, risks, and non-goals are recorded",
            "human review remains part of the operating boundary",
        ],
    }
