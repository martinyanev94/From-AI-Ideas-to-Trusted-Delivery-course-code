from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class PortfolioItem:
    project_id: str
    affected_groups: Sequence[str]
    required_groups: Sequence[str]
    evidence_status: str
    accountable_owner: str
    claim: str
    claim_scope: str


def review_portfolio(items: Sequence[PortfolioItem]) -> dict:
    findings = []
    for item in items:
        missing = sorted(set(item.required_groups) - set(item.affected_groups))
        if missing:
            findings.append({
                "project_id": item.project_id,
                "kind": "missing_affected_group",
                "detail": ", ".join(missing),
            })
        if item.evidence_status != "strong":
            findings.append({
                "project_id": item.project_id,
                "kind": "weak_evidence",
                "detail": item.evidence_status,
            })
        if not item.accountable_owner.strip():
            findings.append({
                "project_id": item.project_id,
                "kind": "unclear_owner",
                "detail": "No accountable owner",
            })
        if item.claim_scope == "production" and item.evidence_status != "strong":
            findings.append({
                "project_id": item.project_id,
                "kind": "unrealistic_claim",
                "detail": item.claim,
            })
    return {"findings": findings}


def governance_outcome(review: dict) -> str:
    blocking = {"missing_affected_group", "unclear_owner", "unrealistic_claim"}
    if any(finding["kind"] in blocking for finding in review["findings"]):
        return "escalate"
    if review["findings"]:
        return "revise"
    return "proceed_bounded"


def review_with_outcome(items: Sequence[PortfolioItem]) -> dict:
    review = review_portfolio(items)
    review["outcome"] = governance_outcome(review)
    return review
