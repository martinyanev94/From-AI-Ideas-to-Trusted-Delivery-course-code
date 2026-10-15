import unittest

from src.review_workflow import (
    InvalidTransition,
    ReviewCase,
    ReviewState,
)


class ReviewWorkflowTests(unittest.TestCase):
    def make_case(self) -> ReviewCase:
        return ReviewCase(
            case_id="case-17",
            affected_person="Jordan",
            decision="reduce scheduled hours",
            rationale="forecasted staffing demand was below target",
        )

    def test_harmful_challenge_escalates_and_records_feedback(self) -> None:
        case = self.make_case()
        case.explain()
        case.challenge(
            "availability record is outdated",
            material_harm=True,
            missing_evidence=True,
        )

        self.assertEqual(case.state, ReviewState.ESCALATED)
        case.resolve("restore hours; availability record was stale")
        case.record_feedback("validate availability before the next schedule")

        self.assertEqual(case.state, ReviewState.FEEDBACK_RECORDED)
        self.assertIn("validate availability", case.feedback)

    def test_challenge_requires_explanation(self) -> None:
        case = self.make_case()
        with self.assertRaises(InvalidTransition):
            case.challenge(
                "incorrect data",
                material_harm=False,
                missing_evidence=True,
            )

    def test_low_risk_challenge_can_be_reviewed_without_escalation(self) -> None:
        case = self.make_case()
        case.explain()
        case.challenge(
            "the rationale needs clarification",
            material_harm=False,
            missing_evidence=False,
        )

        self.assertEqual(case.state, ReviewState.CHALLENGED)


if __name__ == "__main__":
    unittest.main()
