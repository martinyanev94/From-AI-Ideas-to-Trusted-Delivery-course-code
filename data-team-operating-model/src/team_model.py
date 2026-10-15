from dataclasses import dataclass


@dataclass(frozen=True)
class Role:
    name: str
    outcome: str
    responsibilities: tuple[str, ...]
    collaboration_points: tuple[str, ...]

    def validate(self) -> None:
        if not self.name or not self.outcome:
            raise ValueError("role needs a name and outcome")
        if not self.responsibilities or not self.collaboration_points:
            raise ValueError("role needs responsibilities and handoffs")


def validate_team(team: list[Role]) -> None:
    if not team:
        raise ValueError("team must contain at least one role")
    for role in team:
        role.validate()
