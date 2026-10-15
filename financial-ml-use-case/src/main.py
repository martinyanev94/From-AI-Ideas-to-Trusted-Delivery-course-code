from validation_plan import Control, ValidationSlice, recommendation


def main() -> None:
    slices = (
        ValidationSlice(
            name="later-period",
            question="Does performance persist on later periods?",
            evidence="reviewed later-period evaluation record",
            status="pass",
        ),
        ValidationSlice(
            name="material-segment",
            question="Does performance hold across the material segment?",
            evidence="segment evidence is incomplete",
            status="revise",
        ),
        ValidationSlice(
            name="stress",
            question="Does the control remain safe under input stress?",
            evidence="reviewed stress evaluation record",
            status="pass",
        ),
    )
    controls = (
        Control(
            name="human override",
            owner="decision owner",
            trigger="reviewer disputes a ranking",
            response="remove or reorder the item and record the reason",
        ),
        Control(
            name="input completeness",
            owner="model owner",
            trigger="required input is missing",
            response="pause the stage and use the approved fallback",
        ),
    )
    print(recommendation(slices, controls))


if __name__ == "__main__":
    main()
