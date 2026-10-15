import pytest

from src.team_model import Role, validate_team


def test_team_accepts_roles_with_outcomes_and_handoffs():
    team = [
        Role(
            "Analyst",
            "Decision-ready evidence",
            ("define measures",),
            ("frame the question with the service lead",),
        )
    ]

    validate_team(team)


def test_role_without_handoff_is_rejected():
    role = Role("Analyst", "Decision-ready evidence", ("define measures",), ())

    with pytest.raises(ValueError, match="handoffs"):
        role.validate()


def test_empty_team_is_rejected():
    with pytest.raises(ValueError, match="at least one"):
        validate_team([])
