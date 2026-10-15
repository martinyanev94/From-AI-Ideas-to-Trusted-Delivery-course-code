from graph_spec import Graph, Node
from evaluation import GraphApplicationBrief


def main() -> None:
    graph = Graph(
        nodes={
            "case_101": Node("case_101", "billing", "2026-01-10"),
            "case_102": Node("case_102", "billing", "2026-01-08"),
            "case_103": Node("case_103", "billing", "2026-01-09"),
        },
        edges=[("case_101", "case_102"), ("case_101", "case_103")],
    )
    known_labels = {"case_102": 1, "case_103": 0}
    score = graph.neighbor_average("case_101", known_labels)
    prediction = graph.threshold_prediction("case_101", known_labels)
    brief = GraphApplicationBrief(
        task="Predict escalation for a new support case",
        prediction_time="case creation",
        data_requirements=[
            "timestamped case attributes",
            "timestamped relationship creation",
            "labels known before prediction",
        ],
        leakage_risks=[
            "using the target case's later resolution",
            "building edges from post-creation information",
        ],
        limitations=[
            "isolated cases have no neighbor evidence",
            "same-area neighbors may not share outcomes",
        ],
        baseline="case attributes without graph edges",
        recommendation="revise before time-aware baseline evaluation",
    )
    print({"score": score, "prediction": prediction})
    print(brief.as_record())


if __name__ == "__main__":
    main()
