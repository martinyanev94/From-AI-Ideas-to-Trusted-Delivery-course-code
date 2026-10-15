import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from portfolio import PortfolioItem, missing_evidence, render_dashboard

def item(**overrides):
    values = {
        "project_id": "demo",
        "title": "Demo project",
        "value": "measurable outcome",
        "readiness": "pilot",
        "provenance": "source and owner recorded",
        "ethical_risk": "review context required",
        "owner": "service lead",
        "next_decision": "approve pilot",
        "evidence": ["workflow check"],
    }
    values.update(overrides)
    return PortfolioItem(**values)

def test_complete_item_has_no_missing_fields():
    assert missing_evidence(item()) == []

def test_missing_review_fields_are_visible():
    gaps = missing_evidence(item(provenance="", ethical_risk=""))
    assert gaps == ["provenance", "ethical_risk"]
    assert "MISSING: provenance, ethical_risk" in render_dashboard([item(provenance="", ethical_risk="")])

def test_empty_evidence_is_visible():
    assert missing_evidence(item(evidence=[])) == ["evidence"]
    assert "MISSING: evidence" in render_dashboard([item(evidence=[])])

def test_owner_and_next_decision_are_required():
    gaps = missing_evidence(item(owner="", next_decision=""))
    assert gaps == ["owner", "next_decision"]
