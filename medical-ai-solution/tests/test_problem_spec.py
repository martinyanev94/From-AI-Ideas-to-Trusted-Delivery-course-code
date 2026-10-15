import pytest

from src.problem_spec import MedicalAIProblem, example_problem


def test_complete_problem_is_valid():
    problem = example_problem()
    problem.validate()
    assert "urgent-review" not in problem.fallback_action


def test_missing_fallback_is_rejected():
    problem = example_problem()
    incomplete = MedicalAIProblem(
        decision_context=problem.decision_context,
        scientific_question=problem.scientific_question,
        intended_users=problem.intended_users,
        input_data=problem.input_data,
        false_positive_consequence=problem.false_positive_consequence,
        false_negative_consequence=problem.false_negative_consequence,
        fallback_action="",
    )
    with pytest.raises(ValueError):
        incomplete.validate()
