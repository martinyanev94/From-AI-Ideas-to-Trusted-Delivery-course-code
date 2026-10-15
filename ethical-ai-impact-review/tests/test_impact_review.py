import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

import pytest

from impact_review import ImpactItem, build_report


def complete_items():
    return [
        ImpactItem("fairness", "finding", "rationale", "owner"),
        ImpactItem("accuracy", "finding", "rationale", "owner"),
        ImpactItem("fitness", "finding", "rationale", "owner"),
        ImpactItem("accountability", "finding", "rationale", "owner"),
    ]


def test_complete_high_stakes_review_requires_revision_for_open_controls():
    report = build_report(
        "staffing recommendation",
        ["employees"],
        complete_items(),
        ["explained", "challenged", "resolved", "feedback_recorded"],
        ["availability validation"],
    )
    assert report["status"] == "revise"
    assert report["missing_review_states"] == []


def test_missing_dimension_is_rejected():
    with pytest.raises(ValueError, match="missing dimensions"):
        build_report(
            "staffing recommendation",
            ["employees"],
            complete_items()[:3],
            [],
            [],
        )


def test_missing_review_state_requires_revision():
    report = build_report(
        "staffing recommendation",
        ["employees"],
        complete_items(),
        ["explained", "challenged"],
        [],
    )
    assert report["status"] == "revise"
    assert "resolved" in report["missing_review_states"]
