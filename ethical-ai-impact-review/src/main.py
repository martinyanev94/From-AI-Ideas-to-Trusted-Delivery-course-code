from portfolio_review import PortfolioItem, review_with_outcome


items = [
    PortfolioItem(
        project_id="hiring-screen",
        affected_groups=["applicants", "hiring managers"],
        required_groups=["applicants", "hiring managers", "appeals reviewers"],
        evidence_status="partial",
        accountable_owner="Talent operations",
        claim="Supports a bounded pilot",
        claim_scope="bounded_pilot",
    ),
    PortfolioItem(
        project_id="fraud-review",
        affected_groups=["customers", "fraud analysts"],
        required_groups=["customers", "fraud analysts", "appeals reviewers"],
        evidence_status="strong",
        accountable_owner="",
        claim="Ready for production",
        claim_scope="production",
    ),
    PortfolioItem(
        project_id="service-intake",
        affected_groups=["requesters", "analysts"],
        required_groups=["requesters", "analysts"],
        evidence_status="strong",
        accountable_owner="Data service lead",
        claim="Ready for production",
        claim_scope="production",
    ),
]

if __name__ == "__main__":
    print(review_with_outcome(items))
