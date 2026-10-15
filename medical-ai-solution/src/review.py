"""Decision gate for reviewing a medical AI solution package."""


def review_solution(problem, validation, delivery):
    """Return stop, revise, or proceed_bounded for a reviewed proposal."""
    if delivery["stop_condition"] or validation["clinical_safety"] == "stop":
        return "stop"

    required = (
        problem["clinical_fallback"],
        validation["representative_slice"],
        validation["clinical_review"],
        delivery["response_owner"],
        delivery["bounded_scope"],
    )
    return "proceed_bounded" if all(required) else "revise"


if __name__ == "__main__":
    problem = {"clinical_fallback": True}
    validation = {
        "clinical_safety": "review",
        "representative_slice": True,
        "clinical_review": True,
    }
    delivery = {
        "response_owner": "clinical operations",
        "bounded_scope": True,
        "stop_condition": False,
    }
    print(review_solution(problem, validation, delivery))
