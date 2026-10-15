import unittest

from src.service_model import (
    IntakeRequest,
    advance,
    example_request,
    pilot_roles,
    run_example,
    validate_pilot,
)


class ServiceModelTests(unittest.TestCase):
    def test_example_has_complete_role_coverage(self):
        valid, errors = validate_pilot(pilot_roles(), example_request())
        self.assertTrue(valid)
        self.assertEqual(errors, [])

    def test_missing_handoff_owner_is_rejected(self):
        request = IntakeRequest(
            "REQ-002", "review retention", "dashboard", "business_translator", "unknown"
        )
        valid, errors = validate_pilot(pilot_roles(), request)
        self.assertFalse(valid)
        self.assertIn("handoff owner is not covered", errors)

    def test_example_reaches_completed_in_order(self):
        self.assertEqual(
            run_example(), ["accepted", "in_delivery", "reviewed", "completed"]
        )

    def test_invalid_transition_is_rejected(self):
        with self.assertRaises(ValueError):
            advance(IntakeRequest("REQ-003", "outcome", "artifact", "a", "b", "submitted"))


if __name__ == "__main__":
    unittest.main()
