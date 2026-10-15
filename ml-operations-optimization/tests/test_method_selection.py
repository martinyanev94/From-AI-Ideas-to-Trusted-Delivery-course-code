from src.method_selection import (
    delivery_scheduling_record,
    select_method,
)


def test_hybrid_for_forecast_plus_constraints() -> None:
    result = select_method(True, True, True, True)
    assert result.method == "hybrid"
    assert "historical patterns can support prediction" in result.reasons
    assert "the action must satisfy hard constraints" in result.reasons


def test_or_for_known_inputs_and_explicit_rules() -> None:
    result = select_method(False, True, True, False)
    assert result.method == "operations_research"


def test_ml_for_prediction_without_constrained_action() -> None:
    result = select_method(True, False, False, True)
    assert result.method == "machine_learning"


def test_unknown_structure_requires_clarification() -> None:
    result = select_method(False, False, False, False)
    assert result.method == "clarify_problem"


def test_delivery_record_contains_constraints_and_measures() -> None:
    record = delivery_scheduling_record()
    assert record.method == "hybrid"
    assert "each order has one van" in record.constraints
    assert "schedule is feasible" in record.success_measures
