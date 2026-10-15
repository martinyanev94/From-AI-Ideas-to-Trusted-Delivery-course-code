import unittest

from src.portfolio_review import (
    PortfolioItem,
    governance_outcome,
    review_portfolio,
    review_with_outcome,
)


class PortfolioReviewTests(unittest.TestCase):
    def test_finds_missing_group_and_weak_evidence(self):
        item = PortfolioItem(
            project_id="hiring-screen",
            affected_groups=["applicants"],
            required_groups=["applicants", "appeals reviewers"],
            evidence_status="partial",
            accountable_owner="Talent operations",
            claim="Supports a bounded pilot",
            claim_scope="bounded_pilot",
        )

        review = review_portfolio([item])
        kinds = {finding["kind"] for finding in review["findings"]}

        self.assertEqual(kinds, {"missing_affected_group", "weak_evidence"})

    def test_owner_gap_escalates_even_with_strong_evidence(self):
        item = PortfolioItem(
            project_id="fraud-review",
            affected_groups=["customers", "appeals reviewers"],
            required_groups=["customers", "appeals reviewers"],
            evidence_status="strong",
            accountable_owner="",
            claim="Ready for production",
            claim_scope="production",
        )

        review = review_with_outcome([item])

        self.assertEqual(review["outcome"], "escalate")
        self.assertIn("unclear_owner", {f["kind"] for f in review["findings"]})

    def test_weak_production_claim_escalates(self):
        item = PortfolioItem(
            project_id="credit-review",
            affected_groups=["customers", "appeals reviewers"],
            required_groups=["customers", "appeals reviewers"],
            evidence_status="partial",
            accountable_owner="Risk operations",
            claim="Ready for production",
            claim_scope="production",
        )

        review = review_with_outcome([item])

        self.assertEqual(review["outcome"], "escalate")
        self.assertIn("unrealistic_claim", {f["kind"] for f in review["findings"]})

    def test_clean_item_can_proceed_bounded(self):
        item = PortfolioItem(
            project_id="service-intake",
            affected_groups=["requesters", "analysts"],
            required_groups=["requesters", "analysts"],
            evidence_status="strong",
            accountable_owner="Data service lead",
            claim="Ready for production",
            claim_scope="production",
        )

        review = review_with_outcome([item])

        self.assertEqual(review["outcome"], "proceed_bounded")
        self.assertEqual(review["findings"], [])


if __name__ == "__main__":
    unittest.main()
