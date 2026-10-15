from dataclasses import dataclass

PRODUCTION_GATES = (
    "data readiness",
    "operating ownership",
    "operating process",
    "monitoring",
    "sponsor approval",
)


@dataclass
class RoadmapRow:
    priority: str
    use_case: str
    data_dependency: str
    sponsor: str
    funding_assumption: str
    next_decision: str

    def validate(self) -> list[str]:
        fields = {
            "priority": self.priority,
            "use_case": self.use_case,
            "data_dependency": self.data_dependency,
            "sponsor": self.sponsor,
            "funding_assumption": self.funding_assumption,
            "next_decision": self.next_decision,
        }
        return [name for name, value in fields.items() if not value.strip()]


def production_ready(status: dict[str, bool]) -> bool:
    return all(status.get(gate, False) for gate in PRODUCTION_GATES)


def sequence(rows: list[RoadmapRow]) -> list[RoadmapRow]:
    return sorted(rows, key=lambda row: (len(row.validate()) != 0, row.use_case))
