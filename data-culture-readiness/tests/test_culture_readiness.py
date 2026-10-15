from datetime import date

import pytest

from src.culture_readiness import ReadinessGap, prioritize_gaps


def gap(dimension: str, score: int, impact: int = 3, feasibility: int = 3) -> ReadinessGap:
    return ReadinessGap(
        dimension, score, impact, feasibility, "Take the action", "Owner",
        "Observable evidence", date(2026, 11, 14),
    )


def test_lowest_score_is_prioritized_first() -> None:
    result = prioritize_gaps([gap("literacy", 3), gap("sourcing", 1)])
    assert [item.dimension for item in result] == ["sourcing", "literacy"]


def test_impact_breaks_equal_score_ties() -> None:
    result = prioritize_gaps([gap("one", 2, impact=2), gap("two", 2, impact=5)])
    assert [item.dimension for item in result] == ["two", "one"]


def test_invalid_score_is_rejected() -> None:
    with pytest.raises(ValueError, match="score"):
        gap("literacy", 6)
