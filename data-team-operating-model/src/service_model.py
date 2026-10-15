from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class RoleBundle:
    name: str
    outcome: str
    collaboration_point: str


@dataclass(frozen=True)
class IntakeRequest:
    request_id: str
    intended_outcome: str
    deliverable: str
    owner: str
    next_owner: str
    state: str = "submitted"


ALLOWED_TRANSITIONS: Dict[str, str] = {
    "submitted": "accepted",
    "accepted": "in_delivery",
    "in_delivery": "reviewed",
    "reviewed": "completed",
}


def validate_pilot(
    roles: List[RoleBundle], request: IntakeRequest
) -> Tuple[bool, List[str]]:
    role_names = {role.name for role in roles}
    errors: List[str] = []
    if request.owner not in role_names:
        errors.append("request owner is not covered")
    if request.next_owner not in role_names:
        errors.append("handoff owner is not covered")
    if not request.intended_outcome:
        errors.append("intended outcome is required")
    if not request.deliverable:
        errors.append("deliverable is required")
    if request.state not in {"submitted", *ALLOWED_TRANSITIONS.values()}:
        errors.append(f"unknown request state: {request.state}")
    return not errors, errors


def advance(request: IntakeRequest) -> IntakeRequest:
    next_state = ALLOWED_TRANSITIONS.get(request.state)
    if next_state is None:
        raise ValueError(f"no transition from {request.state}")
    return IntakeRequest(
        request_id=request.request_id,
        intended_outcome=request.intended_outcome,
        deliverable=request.deliverable,
        owner=request.owner,
        next_owner=request.next_owner,
        state=next_state,
    )


def pilot_roles() -> List[RoleBundle]:
    return [
        RoleBundle("service_lead", "prioritize requests", "business review"),
        RoleBundle("business_translator", "clarify outcomes", "request intake"),
        RoleBundle("data_engineer", "maintain refresh", "failure response"),
        RoleBundle("analyst", "deliver reviewed insight", "decision brief"),
    ]


def example_request() -> IntakeRequest:
    return IntakeRequest(
        request_id="REQ-001",
        intended_outcome="support leadership can review retention weekly",
        deliverable="weekly retention dashboard",
        owner="business_translator",
        next_owner="data_engineer",
    )


def run_example() -> List[str]:
    request = example_request()
    valid, errors = validate_pilot(pilot_roles(), request)
    if not valid:
        raise ValueError("invalid example request: " + "; ".join(errors))
    states = []
    while request.state != "completed":
        request = advance(request)
        states.append(request.state)
    return states
