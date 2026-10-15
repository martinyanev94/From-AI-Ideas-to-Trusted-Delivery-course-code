from dataclasses import dataclass
from typing import Literal, Sequence

SliceStatus = Literal["pass", "revise", "stop"]


@dataclass(frozen=True)
class ValidationSlice:
    name: str
    question: str
    evidence: str
    status: SliceStatus


@dataclass(frozen=True)
class Control:
    name: str
    owner: str
    trigger: str
    response: str


@dataclass(frozen=True)
class ImplementationStage:
    name: str
    exposure: str
    entry_criteria: tuple[str, ...]
    exit_criteria: tuple[str, ...]


def validate_slice(item: ValidationSlice) -> None:
    if not item.name or not item.question or not item.evidence:
        raise ValueError("slice metadata is incomplete")
    if item.status not in {"pass", "revise", "stop"}:
        raise ValueError("unknown slice status")


def validate_control(item: Control) -> None:
    if not item.name or not item.owner or not item.trigger or not item.response:
        raise ValueError("control must include name, owner, trigger, and response")


def recommendation(
    slices: Sequence[ValidationSlice], controls: Sequence[Control]
) -> str:
    for item in slices:
        validate_slice(item)
    for item in controls:
        validate_control(item)

    if any(item.status == "stop" for item in slices):
        return "stop"
    if any(item.status == "revise" for item in slices):
        return "revise"
    if not controls:
        return "revise"
    return "proceed"


STAGES = (
    ImplementationStage(
        name="shadow evaluation",
        exposure="no operational decision change",
        entry_criteria=("use case approved", "data use recorded"),
        exit_criteria=("all validation slices reviewed", "explanations inspected"),
    ),
    ImplementationStage(
        name="controlled pilot",
        exposure="limited operational scope with human override",
        entry_criteria=("shadow evidence passes", "rollback path tested"),
        exit_criteria=("monitoring response exercised", "decision owner signs off"),
    ),
    ImplementationStage(
        name="broader operation",
        exposure="approved operational scope",
        entry_criteria=("pilot controls pass", "stop conditions monitored"),
        exit_criteria=("operating review scheduled", "ownership transferred"),
    ),
)
