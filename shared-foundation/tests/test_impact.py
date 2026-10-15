import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

import pytest

from impact import ImpactAssessment, ImpactCheck, build_report


def complete_assessment() -> ImpactAssessment:
    assessment = ImpactAssessment(
        use_case="Support-call routing forecast",
        context="Estimate queue volume for staffing allocation.",
        affected_people=["customers", "support agents", "operations managers"],
    )
    for dimension in (
        "context",
        "affected_people",
        "fairness",
        "accuracy",
        "fitness_for_purpose",
        "accountability",
    ):
        assessment.add_check(
            ImpactCheck(
                dimension=dimension,
                status="review" if dimension in {"fairness", "accuracy"} else "pass",
                rationale="Evidence and ownership are documented for review.",
                owner="operations lead",
            )
        )
    return assessment


def test_build_report_requires_all_dimensions():
    report = build_report(complete_assessment())
    assert report["use_case"] == "Support-call routing forecast"
    assert len(report["checks"]) == 6


def test_invalid_status_is_rejected():
    assessment = ImpactAssessment("Example", "Example context")
    with pytest.raises(ValueError, match="invalid status"):
        assessment.add_check(ImpactCheck("accuracy", "unknown", "reason", "owner"))


def test_missing_dimension_is_rejected():
    assessment = ImpactAssessment("Example", "Example context")
    assessment.add_check(ImpactCheck("accuracy", "review", "reason", "owner"))
    with pytest.raises(ValueError, match="missing"):
        build_report(assessment)
