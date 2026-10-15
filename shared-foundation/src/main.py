import json
from pathlib import Path

from provenance import ProvenanceLink


link = ProvenanceLink(
    input_name="interval_call_volume",
    source_system="telephony_platform",
    owner="workforce_planning",
    purpose="forecast incoming calls by interval",
    decision="route_and_staff_calls",
    quality_notes="Interval definition and late-arriving calls need confirmation.",
    evidence_links=("metric_definition", "pipeline_runbook"),
    trust_gap=(
        "Operations report uses a different call-count definition; compare "
        "definitions, extraction, and timing before using the forecast for routing."
    ),
)

if not link.is_actionable():
    raise SystemExit("Provenance record is incomplete")

output_path = Path("provenance_map.json")
output_path.write_text(json.dumps(link.as_dict(), indent=2) + "\n")
print(f"Saved {output_path}")
