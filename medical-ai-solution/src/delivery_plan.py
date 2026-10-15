from dataclasses import dataclass
from typing import Dict, List


@dataclass
class DeliveryPlan:
    clinical_reviewer: str
    deployment_owner: str
    workflow_owner: str
    response_owner: str
    feedback_route: str
    safeguards: List[str]
    review_days: int

    def validate(self) -> List[str]:
        errors: List[str] = []
        if not self.clinical_reviewer:
            errors.append("clinical reviewer required")
        if not self.deployment_owner:
            errors.append("deployment owner required")
        if not self.workflow_owner:
            errors.append("workflow owner required")
        if not self.response_owner:
            errors.append("response owner required")
        if not self.feedback_route:
            errors.append("feedback route required")
        if "stop" not in self.safeguards:
            errors.append("stop safeguard required")
        if "rollback" not in self.safeguards:
            errors.append("rollback safeguard required")
        if self.review_days <= 0:
            errors.append("review interval must be positive")
        return errors


def record_feedback(plan: DeliveryPlan, observation: str) -> Dict[str, str]:
    if not observation:
        raise ValueError("observation required")
    return {
        "observation": observation,
        "route": plan.feedback_route,
        "reviewer": plan.clinical_reviewer,
        "response_owner": plan.response_owner,
    }


def review_due(plan: DeliveryPlan, days_since_review: int) -> bool:
    if days_since_review < 0:
        raise ValueError("days_since_review cannot be negative")
    return days_since_review >= plan.review_days
