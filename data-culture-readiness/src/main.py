from datetime import date

from culture_readiness import ReadinessGap, readiness_plan


gaps = [
    ReadinessGap(
        "sourcing support", 1, 5, 4,
        "Publish intake boundaries and assign a response owner",
        "Data service owner",
        "Boundary published; 90% of in-boundary requests have an owner, response date, and response within 5 business days",
        date(2026, 11, 14),
    ),
    ReadinessGap(
        "collaboration", 2, 5, 3,
        "Require a data partner and decision before project approval",
        "Portfolio sponsor",
        "Approved intakes contain both fields",
        date(2026, 12, 14),
    ),
    ReadinessGap(
        "leadership behavior", 2, 4, 4,
        "Add a decision-and-data check to the weekly leadership review",
        "Data leader",
        "Two consecutive reviews record the check",
        date(2027, 1, 14),
    ),
    ReadinessGap(
        "literacy", 3, 3, 3,
        "Add source, limitation, and permitted-use prompts to intake",
        "Business translator",
        "Project leads complete all three prompts",
        date(2027, 2, 14),
    ),
    ReadinessGap(
        "responsible decision-making", 3, 5, 2,
        "Record affected people and review path for high-stakes requests",
        "Data steward",
        "High-stakes requests contain a review path",
        date(2027, 2, 28),
    ),
]

for row in readiness_plan(gaps):
    print(f"{row['priority']}. {row['dimension']} — {row['action']}")
    print(f"   Owner: {row['owner']} | Evidence: {row['evidence']} | Review: {row['review_date']}")
