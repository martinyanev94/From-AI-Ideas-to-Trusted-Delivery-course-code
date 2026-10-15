from dataclasses import dataclass


@dataclass(frozen=True)
class MethodSelection:
    method: str
    reasons: tuple[str, ...]


def select_method(
    needs_prediction: bool,
    has_hard_constraints: bool,
    has_explicit_rules: bool,
    has_historical_examples: bool,
) -> MethodSelection:
    reasons: list[str] = []
    if needs_prediction and has_historical_examples:
        reasons.append("historical patterns can support prediction")
    if has_hard_constraints:
        reasons.append("the action must satisfy hard constraints")
    if needs_prediction and has_hard_constraints:
        return MethodSelection("hybrid", tuple(reasons))
    if has_hard_constraints and has_explicit_rules:
        return MethodSelection("operations_research", tuple(reasons))
    if needs_prediction and has_historical_examples:
        return MethodSelection("machine_learning", tuple(reasons))
    return MethodSelection("clarify_problem", tuple(reasons))


@dataclass(frozen=True)
class SchedulingDecision:
    problem: str
    method: str
    constraints: tuple[str, ...]
    success_measures: tuple[str, ...]


def delivery_scheduling_record() -> SchedulingDecision:
    selection = select_method(True, True, True, True)
    return SchedulingDecision(
        problem="assign tomorrow's orders to two vans",
        method=selection.method,
        constraints=(
            "each order has one van",
            "van capacity is not exceeded",
            "delivery windows do not overlap",
        ),
        success_measures=(
            "forecast error is tracked",
            "schedule is feasible",
            "on-time delivery improves",
        ),
    )
