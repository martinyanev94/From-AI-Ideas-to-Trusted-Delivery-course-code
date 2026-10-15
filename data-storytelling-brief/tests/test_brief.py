import pytest

from src.brief import Brief


@pytest.fixture
def complete_brief() -> Brief:
    return Brief(
        context="Routing delays affect support operations.",
        evidence="The historical sample reduced median assignment time by 22%.",
        limitations="The sample covers one region and historical tickets.",
        decision="revise",
        action="Run a bounded pilot and review urgent-ticket misrouting daily.",
    )


def test_render_contains_all_decision_sections(complete_brief: Brief) -> None:
    rendered = complete_brief.render()

    for heading in (
        "## Context",
        "## Evidence",
        "## Limitations",
        "## Decision",
        "## Recommended action",
    ):
        assert heading in rendered


def test_missing_limitations_are_rejected(complete_brief: Brief) -> None:
    complete_brief.limitations = ""

    with pytest.raises(ValueError, match="limitations"):
        complete_brief.render()
