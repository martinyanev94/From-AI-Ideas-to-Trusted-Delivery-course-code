import unittest

from src.review import review_solution


class ReviewSolutionTests(unittest.TestCase):
    def setUp(self):
        self.problem = {"clinical_fallback": True}
        self.validation = {
            "clinical_safety": "review",
            "representative_slice": True,
            "clinical_review": True,
        }
        self.delivery = {
            "response_owner": "clinical operations",
            "bounded_scope": True,
            "stop_condition": False,
        }

    def test_complete_package_allows_bounded_evaluation(self):
        self.assertEqual(
            review_solution(self.problem, self.validation, self.delivery),
            "proceed_bounded",
        )

    def test_missing_fallback_requires_revision(self):
        self.problem["clinical_fallback"] = False
        self.assertEqual(
            review_solution(self.problem, self.validation, self.delivery),
            "revise",
        )

    def test_stop_condition_takes_precedence(self):
        self.delivery["stop_condition"] = True
        self.assertEqual(
            review_solution(self.problem, self.validation, self.delivery),
            "stop",
        )


if __name__ == "__main__":
    unittest.main()
