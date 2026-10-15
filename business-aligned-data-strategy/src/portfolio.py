from dataclasses import dataclass
from typing import List
import json

@dataclass(frozen=True)
class PortfolioItem:
    project_id: str
    title: str
    value: str
    readiness: str
    provenance: str
    ethical_risk: str
    owner: str
    next_decision: str
    evidence: List[str]

def missing_evidence(item: PortfolioItem) -> List[str]:
    missing = []
    for field in ("value", "readiness", "provenance", "ethical_risk", "owner", "next_decision"):
        if not getattr(item, field).strip():
            missing.append(field)
    if not item.evidence:
        missing.append("evidence")
    return missing

def load_items(path: str) -> List[PortfolioItem]:
    with open(path, encoding="utf-8") as handle:
        rows = json.load(handle)
    return [PortfolioItem(**row) for row in rows]

def render_dashboard(items: List[PortfolioItem]) -> str:
    lines = ["PORTFOLIO REVIEW"]
    for item in items:
        gaps = missing_evidence(item)
        status = "OK" if not gaps else "MISSING: " + ", ".join(gaps)
        lines.append(
            f"{item.title} | {item.value} | {item.readiness} | "
            f"{item.provenance} | {item.ethical_risk} | {item.owner} | "
            f"{item.next_decision} | {status}"
        )
    return "\n".join(lines)
