import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from provenance import ProvenanceLink


def test_complete_link_is_actionable():
    link = ProvenanceLink(
        input_name="interval_call_volume",
        source_system="telephony_platform",
        owner="workforce_planning",
        purpose="forecast incoming calls by interval",
        decision="route_and_staff_calls",
        quality_notes="Definition needs confirmation.",
        evidence_links=("metric_definition",),
        trust_gap="Operations report uses a different definition.",
    )

    assert link.is_actionable() is True


def test_missing_trust_gap_is_not_actionable():
    link = ProvenanceLink(
        input_name="interval_call_volume",
        source_system="telephony_platform",
        owner="workforce_planning",
        purpose="forecast incoming calls by interval",
        decision="route_and_staff_calls",
        quality_notes="Definition needs confirmation.",
        evidence_links=("metric_definition",),
        trust_gap="",
    )

    assert link.is_actionable() is False
