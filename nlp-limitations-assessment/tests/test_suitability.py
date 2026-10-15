import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from suitability import NLPProposal, assess


class SuitabilityTests(unittest.TestCase):
    def make_proposal(self, **overrides):
        values = {
            "name": "support urgency routing",
            "intended_outcome": "flag messages for human urgent review",
            "input_description": "customer message text",
            "ambiguity_examples": ("sarcasm",),
            "evidence_requirements": ("held-out evaluation set",),
            "risks": ("missed urgency",),
            "non_goals": ("no unsupervised response",),
            "human_review_required": True,
        }
        values.update(overrides)
        return NLPProposal(**values)

    def test_complete_proposal_can_enter_bounded_evaluation(self):
        result = assess(self.make_proposal())
        self.assertEqual(result["recommendation"], "proceed to bounded evaluation")

    def test_missing_ambiguity_is_a_revision_reason(self):
        result = assess(self.make_proposal(ambiguity_examples=()))
        self.assertEqual(result["recommendation"], "revise")
        self.assertIn("missing: ambiguity_examples", result["reasons"])

    def test_no_human_review_requires_revision(self):
        result = assess(self.make_proposal(human_review_required=False))
        self.assertEqual(result["recommendation"], "revise")
        self.assertIn("human review", result["reasons"][0])


if __name__ == "__main__":
    unittest.main()
