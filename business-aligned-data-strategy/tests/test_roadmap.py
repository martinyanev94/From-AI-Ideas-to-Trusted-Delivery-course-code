import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from roadmap import PRODUCTION_GATES, RoadmapRow, production_ready


def test_complete_row_has_no_validation_errors():
    row = RoadmapRow("priority", "use case", "dependency", "sponsor", "funding", "decision")
    assert row.validate() == []


def test_missing_sponsor_is_reported():
    row = RoadmapRow("priority", "use case", "dependency", "", "funding", "decision")
    assert row.validate() == ["sponsor"]


def test_all_gates_are_required():
    complete = {gate: True for gate in PRODUCTION_GATES}
    assert production_ready(complete)
    complete["monitoring"] = False
    assert not production_ready(complete)
