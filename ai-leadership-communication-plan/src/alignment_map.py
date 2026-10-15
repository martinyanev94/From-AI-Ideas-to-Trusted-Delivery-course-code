from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class StakeholderRecord:
    name: str
    role: str
    stated_need: str
    hidden_incentive: str
    objection: str
    influence_paths: tuple[str, ...]
    communication_owner: str

    def validate(self) -> None:
        fields = (
            self.name,
            self.role,
            self.stated_need,
            self.hidden_incentive,
            self.objection,
            self.communication_owner,
        )
        if any(not field.strip() for field in fields):
            raise ValueError("stakeholder fields cannot be blank")
        if not self.influence_paths:
            raise ValueError("at least one influence path is required")
        if any(not path.strip() for path in self.influence_paths):
            raise ValueError("influence paths cannot be blank")


def build_map(records: Iterable[StakeholderRecord]) -> list[StakeholderRecord]:
    mapped = list(records)
    for record in mapped:
        record.validate()
    return mapped


def unresolved_objections(records: Iterable[StakeholderRecord]) -> list[str]:
    return [record.name for record in records if record.objection.strip()]
