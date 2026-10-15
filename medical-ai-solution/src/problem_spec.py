from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class MedicalAIProblem:
    decision_context: str
    scientific_question: str
    intended_users: Tuple[str, ...]
    input_data: Tuple[str, ...]
    false_positive_consequence: str
    false_negative_consequence: str
    fallback_action: str

    def validate(self) -> None:
        required = (
            self.decision_context,
            self.scientific_question,
            self.false_positive_consequence,
            self.false_negative_consequence,
            self.fallback_action,
        )
        if any(not value.strip() for value in required):
            raise ValueError("clinical problem fields cannot be empty")
        if not self.intended_users or not self.input_data:
            raise ValueError("users and inputs must be specified")


def example_problem() -> MedicalAIProblem:
    return MedicalAIProblem(
        decision_context="Dermatology visit: prioritize specialist assessment for a lesion",
        scientific_question="Can clinic-captured images support urgent-review decisions?",
        intended_users=("dermatology clinician",),
        input_data=("lesion image", "image quality status", "visit setting"),
        false_positive_consequence="Unnecessary urgent referral and use of specialist capacity",
        false_negative_consequence="Delayed assessment of a potentially serious lesion",
        fallback_action="Do not recommend; retake the image or use manual assessment",
    )


if __name__ == "__main__":
    problem = example_problem()
    problem.validate()
    print(problem.decision_context)
