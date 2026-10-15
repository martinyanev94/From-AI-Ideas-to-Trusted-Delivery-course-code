from src.validation_plan import ValidationPlan, ValidationSlice


def complete_plan() -> ValidationPlan:
    return ValidationPlan(
        slices=(
            ValidationSlice("neurology clinic", "intended patients", "clinic", True),
            ValidationSlice("older adults", "older adults", "clinic", True),
            ValidationSlice("incomplete histories", "incomplete histories", "clinic", True),
        ),
        clinical_reviewers=("neurologist", "nurse reviewer"),
        team_expertise=("clinical", "data", "engineering", "governance"),
        fallback_action="route uncertain cases to ordinary clinical review",
        response_owner="clinical operations lead",
        reviewer_can_stop=True,
        stages_completed=("data", "clinical", "workflow"),
    )


def test_complete_plan_reaches_bounded_evaluation():
    plan = complete_plan()
    assert plan.validate() == ()
    assert plan.recommendation() == "bounded evaluation"


def test_missing_prediction_time_inputs_are_named():
    plan = complete_plan()
    slices = (*plan.slices[:-1], ValidationSlice(
        "incomplete histories", "incomplete histories", "clinic", False
    ))
    invalid = ValidationPlan(
        slices=slices,
        clinical_reviewers=plan.clinical_reviewers,
        team_expertise=plan.team_expertise,
        fallback_action=plan.fallback_action,
        response_owner=plan.response_owner,
        reviewer_can_stop=plan.reviewer_can_stop,
        stages_completed=plan.stages_completed,
    )
    assert "prediction-time inputs missing for incomplete histories" in invalid.validate()
    assert invalid.recommendation() == "revise"


def test_reviewers_need_stop_authority():
    plan = complete_plan()
    invalid = ValidationPlan(
        slices=plan.slices,
        clinical_reviewers=plan.clinical_reviewers,
        team_expertise=plan.team_expertise,
        fallback_action=plan.fallback_action,
        response_owner=plan.response_owner,
        reviewer_can_stop=False,
        stages_completed=plan.stages_completed,
    )
    assert "clinical reviewers cannot stop advancement" in invalid.validate()
    assert invalid.recommendation() == "revise"


def test_incomplete_ordered_stages_continue_validation():
    plan = complete_plan()
    partial = ValidationPlan(
        slices=plan.slices,
        clinical_reviewers=plan.clinical_reviewers,
        team_expertise=plan.team_expertise,
        fallback_action=plan.fallback_action,
        response_owner=plan.response_owner,
        reviewer_can_stop=True,
        stages_completed=("data", "clinical"),
    )
    assert partial.validate() == ()
    assert partial.recommendation() == "continue validation"
