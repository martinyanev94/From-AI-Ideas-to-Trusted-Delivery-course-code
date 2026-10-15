import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from diagnostic import RecoveryAction, build_example, recovery_status


def test_example_is_complete():
    assert build_example().validate() == []


def test_guardrail_failure_requires_revision():
    action = build_example()
    assert recovery_status(action, outcome_improved=True, guardrail_holds=False) == "revise"


def test_missing_evidence_is_invalid():
    action = RecoveryAction("cause", "intervention", "owner", ["one"], "outcome", "leading", "guardrail", "rule")
    assert "at least two evidence items are required" in action.validate()
