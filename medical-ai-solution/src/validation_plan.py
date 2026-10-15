from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class ValidationSlice:
    name: str
    population: str
    setting: str
    inputs_available: bool


@dataclass(frozen=True)
class ValidationPlan:
    slices: Tuple[ValidationSlice, ...]
    clinical_reviewers: Tuple[str, ...]
    team_expertise: Tuple[str, ...]
    fallback_action: str
    response_owner: str
    reviewer_can_stop: bool
    stages_completed: Tuple[str, ...]

    def validate(self) -> Tuple[str, ...]:
        errors = []
        if not self.slices:
            errors.append("at least one validation slice is required")
        for item in self.slices:
            if not item.name or not item.population or not item.setting:
                errors.append("each slice needs name, population, and setting")
            if not item.inputs_available:
                errors.append(f"prediction-time inputs missing for {item.name}")
        if not self.clinical_reviewers:
            errors.append("clinical review is not assigned")
        if not self.team_expertise:
            errors.append("team expertise is not represented")
        if not self.fallback_action:
            errors.append("fallback action is not defined")
        if not self.response_owner:
            errors.append("deployment response owner is not defined")
        if not self.reviewer_can_stop:
            errors.append("clinical reviewers cannot stop advancement")

        required = ("data", "clinical", "workflow")
        if any(stage not in required for stage in self.stages_completed):
            errors.append("unknown validation stage recorded")
        if self.stages_completed != tuple(
            stage for stage in required if stage in self.stages_completed
        ):
            errors.append("validation stages must be completed in order")
        return tuple(errors)

    def recommendation(self) -> str:
        if self.validate():
            return "revise"
        if self.stages_completed == ("data", "clinical", "workflow"):
            return "bounded evaluation"
        return "continue validation"
