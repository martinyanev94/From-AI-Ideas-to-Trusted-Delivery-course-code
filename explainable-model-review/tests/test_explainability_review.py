from src.explainability_review import (
    ExplanationRequirement,
    build_requirements,
    render_report,
    review_requirements,
)


def test_default_requirements_are_ready():
    report = render_report(build_requirements())
    assert report["status"] == "proceed"
    assert report["gaps"] == []
    assert len(report["requirements"]) == 3


def test_mismatched_auditor_explanation_requires_revision():
    requirements = build_requirements()
    requirements[2] = ExplanationRequirement(
        "auditor", "high", "verify consistency and accountability",
        "feature importance chart", "deep", "audit owner",
        "request evidence review", "technical verification", "governance lead",
        "correct or withdraw the recommendation", "resolved",
    )
    report = review_requirements(requirements)
    assert report["status"] == "revise"
    assert "auditor: accessible rationale and technical trace are required" in report["gaps"]


def test_missing_owner_is_reported_as_unresolved_control():
    requirements = build_requirements()
    requirements[0] = ExplanationRequirement(
        "affected_person", "high", "understand and challenge the outcome",
        "plain-language reason and relevant factors", "deep", "",
        "submit challenge", "human case review", "appeals lead",
        "correct decision when error is confirmed", "resolved",
    )
    report = review_requirements(requirements)
    assert report["status"] == "revise"
    assert "affected_person: accountability control remains unresolved" in report["gaps"]


def test_high_stakes_light_review_requires_revision():
    requirements = build_requirements()
    item = requirements[2]
    requirements[2] = ExplanationRequirement(
        item.stakeholder_role, item.decision_stakes, item.accountability_need,
        item.explanation_type, "light", item.accountable_owner,
        item.challenge_action, item.human_check, item.escalation_path,
        item.correction_action, item.resolution_state,
    )
    report = review_requirements(requirements)
    assert report["status"] == "revise"
    assert "auditor: review is too shallow" in report["gaps"]
