import json

from service_model import example_request, pilot_roles, run_example, validate_pilot


def main() -> None:
    request = example_request()
    valid, errors = validate_pilot(pilot_roles(), request)
    result = {
        "request_id": request.request_id,
        "valid": valid,
        "errors": errors,
        "states": run_example() if valid else [],
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
