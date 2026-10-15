from diagnostic import build_example, recovery_status


def main() -> None:
    action = build_example()
    print(action)
    print("validation:", action.validate() or "ok")
    print("status with improved outcome and holding guardrail:", recovery_status(action, True, True))


if __name__ == "__main__":
    main()
