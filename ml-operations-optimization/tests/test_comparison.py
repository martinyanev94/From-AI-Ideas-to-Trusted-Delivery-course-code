import pytest

from src.comparison import ApproachResult, compare


def test_ineligible_result_cannot_win_on_headline_metric():
    results = [
        ApproachResult("predictive", "partial", "medium", False, 1.0, 0),
        ApproachResult("optimization", "high", "high", True, 2 / 3, 60),
    ]

    assert compare(results).approach == "optimization"


def test_feasible_results_use_operational_measures_after_requirements():
    results = [
        ApproachResult("optimization", "high", "high", True, 0.8, 40),
        ApproachResult("hybrid", "high", "high", True, 0.8, 20),
    ]

    assert compare(results).approach == "hybrid"


def test_empty_comparison_is_rejected():
    with pytest.raises(ValueError, match="at least one"):
        compare([])


def test_no_eligible_approach_is_rejected():
    with pytest.raises(ValueError, match="no approach"):
        compare([ApproachResult("predictive", "partial", "medium", False, 1.0, 0)])


def test_rate_and_lateness_are_validated():
    with pytest.raises(ValueError):
        ApproachResult("predictive", "low", "low", False, 1.1, 0)
    with pytest.raises(ValueError):
        ApproachResult("optimization", "high", "high", True, 0.5, -1)
