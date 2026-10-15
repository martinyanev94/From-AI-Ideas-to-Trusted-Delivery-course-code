import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from use_case import UseCaseSpecification


def test_complete_use_case_is_valid():
    specification = UseCaseSpecification(
        decision="Which tickets need follow-up first?",
        stakeholder="Support Operations",
        intended_outcome="Prioritize follow-up consistently.",
        success_signal="Lower median ticket age.",
        guardrail_metric="No increase in reopened tickets.",
    )
    assert specification.validate() == []
