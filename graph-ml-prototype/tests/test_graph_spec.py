import unittest

from src.evaluation import GraphApplicationBrief
from src.graph_spec import Graph, Node


class GraphEvaluationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = Graph(
            nodes={
                "case_101": Node("case_101", "billing", "2026-01-10"),
                "case_102": Node("case_102", "billing", "2026-01-08"),
                "case_103": Node("case_103", "billing", "2026-01-09"),
                "case_104": Node("case_104", "shipping", "2026-01-10"),
            },
            edges=[("case_101", "case_102"), ("case_101", "case_103")],
        )

    def test_neighbor_average_and_threshold(self) -> None:
        labels = {"case_102": 1, "case_103": 0}
        self.assertEqual(self.graph.neighbor_average("case_101", labels), 0.5)
        self.assertEqual(self.graph.threshold_prediction("case_101", labels), 1)

    def test_isolated_node_has_no_graph_evidence(self) -> None:
        self.assertIsNone(self.graph.neighbor_average("case_104", {}))
        self.assertIsNone(self.graph.threshold_prediction("case_104", {}))

    def test_brief_requires_evaluation_sections(self) -> None:
        brief = GraphApplicationBrief("task", "creation", ["nodes"], ["future label"], ["isolated nodes"], "tabular", "revise")
        self.assertEqual(brief.as_record()["recommendation"], "revise")


if __name__ == "__main__":
    unittest.main()
