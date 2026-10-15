from dataclasses import dataclass
from itertools import product
from typing import Mapping


@dataclass(frozen=True)
class Delivery:
    name: str
    allowed_slots: tuple[int, ...]
    travel_minutes: Mapping[int, int]


@dataclass(frozen=True)
class Schedule:
    assignments: Mapping[str, int]


def feasibility_errors(
    deliveries: Mapping[str, Delivery],
    schedule: Schedule,
    capacity: int,
) -> list[str]:
    errors: list[str] = []
    if set(schedule.assignments) != set(deliveries):
        errors.append("each delivery must be assigned exactly once")

    slot_counts: dict[int, int] = {}
    for name, delivery in deliveries.items():
        slot = schedule.assignments.get(name)
        if slot not in delivery.allowed_slots:
            errors.append(f"{name} is outside its delivery window")
        if slot is not None:
            slot_counts[slot] = slot_counts.get(slot, 0) + 1

    for slot, count in slot_counts.items():
        if count > capacity:
            errors.append(f"slot {slot} exceeds capacity {capacity}")
    return errors


def total_travel_minutes(
    deliveries: Mapping[str, Delivery],
    schedule: Schedule,
) -> int:
    return sum(
        deliveries[name].travel_minutes[slot]
        for name, slot in schedule.assignments.items()
    )


def best_schedule(
    deliveries: Mapping[str, Delivery], capacity: int
) -> Schedule:
    names = tuple(deliveries)
    choices = (deliveries[name].allowed_slots for name in names)
    candidates = (
        Schedule(dict(zip(names, slots)))
        for slots in product(*choices)
    )
    feasible = [
        candidate
        for candidate in candidates
        if not feasibility_errors(deliveries, candidate, capacity)
    ]
    if not feasible:
        raise ValueError("no feasible schedule exists")
    return min(
        feasible,
        key=lambda item: total_travel_minutes(deliveries, item),
    )


def operational_metrics(
    deliveries: Mapping[str, Delivery],
    schedule: Schedule,
    capacity: int,
) -> dict[str, float | bool]:
    errors = feasibility_errors(deliveries, schedule, capacity)
    on_time = sum(
        schedule.assignments.get(name) in delivery.allowed_slots
        for name, delivery in deliveries.items()
    ) / len(deliveries)
    return {
        "feasible": not errors,
        "total_travel_minutes": total_travel_minutes(deliveries, schedule),
        "on_time_rate": on_time,
    }
