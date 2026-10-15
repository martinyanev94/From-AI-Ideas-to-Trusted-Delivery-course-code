from review_workflow import FeedbackRegister, ReviewCase


def main() -> None:
    case = ReviewCase(
        case_id="case-17",
        affected_person="Jordan",
        decision="reduce scheduled hours",
        rationale="forecasted staffing demand was below target",
    )
    case.explain()
    case.challenge(
        "availability record is outdated",
        material_harm=True,
        missing_evidence=True,
    )
    case.resolve("restore hours; availability record was stale")
    case.record_feedback("validate availability before the next schedule")

    register = FeedbackRegister()
    register.add(case)
    print(case.state.value)
    print(register.entries[0])


if __name__ == "__main__":
    main()
