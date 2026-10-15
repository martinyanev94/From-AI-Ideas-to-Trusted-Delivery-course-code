import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from metrics import (  # noqa: E402
    Delivery,
    Schedule,
    best_schedule,
    feasibility_errors,
    operational_metrics,
)


DELIVERIES = {
    "north": Delivery("north", (9, 10), {9: 14, 10: 10}),
    "south": Delivery("south", (9, 10), {9: 9, 10: 12}),
    "east": Delivery("east", (9, 10), {9: 11, 10: 8}),
}


def test_best_schedule_is_feasible_and_minimizes_travel():
    schedule = best_schedule(DELIVERIES, capacity=2)

    assert schedule.assignments == {"north": 10, "south": 9, "east": 10}
    assert operational_metrics(DELIVERIES, schedule, 2) == {
        "feasible": True,
        "total_travel_minutes": 27,
        "on_time_rate": 1.0,
    }


def test_capacity_is_a_hard_constraint():
    overloaded = Schedule({"north": 10, "south": 10, "east": 10})

    assert feasibility_errors(DELIVERIES, overloaded, capacity=2) == [
        "slot 10 exceeds capacity 2"
    ]


def test_impossible_windows_raise_a_clear_error():
    restricted = {
        "north": Delivery("north", (9,), {9: 14}),
        "south": Delivery("south", (9,), {9: 9}),
        "east": Delivery("east", (9,), {9: 11}),
    }

    try:
        best_schedule(restricted, capacity=2)
    except ValueError as error:
        assert str(error) == "no feasible schedule exists"
    else:
        raise AssertionError("expected an infeasible model to raise ValueError")
