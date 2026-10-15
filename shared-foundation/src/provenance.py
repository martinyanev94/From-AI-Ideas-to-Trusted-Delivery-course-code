from dataclasses import dataclass


@dataclass(frozen=True)
class ProvenanceLink:
    input_name: str
    source_system: str
    owner: str
    purpose: str
    decision: str
    quality_notes: str
    evidence_links: tuple[str, ...]
    trust_gap: str

    def is_actionable(self) -> bool:
        return bool(
            self.input_name
            and self.source_system
            and self.owner
            and self.purpose
            and self.decision
            and self.quality_notes
            and self.evidence_links
            and self.trust_gap
        )

    def as_dict(self) -> dict[str, object]:
        return {
            "input_name": self.input_name,
            "source_system": self.source_system,
            "owner": self.owner,
            "purpose": self.purpose,
            "decision": self.decision,
            "quality_notes": self.quality_notes,
            "evidence_links": list(self.evidence_links),
            "trust_gap": self.trust_gap,
        }
