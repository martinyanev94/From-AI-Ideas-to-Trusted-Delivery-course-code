from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class Node:
    node_id: str
    product_area: str
    created_at: str


@dataclass(frozen=True)
class Graph:
    nodes: Dict[str, Node]
    edges: List[Tuple[str, str]]

    def neighbor_average(self, node_id: str, known_labels: Dict[str, int]) -> Optional[float]:
        neighbors = [
            right if left == node_id else left
            for left, right in self.edges
            if left == node_id or right == node_id
        ]
        values = [known_labels[neighbor] for neighbor in neighbors if neighbor in known_labels]
        return None if not values else sum(values) / len(values)

    def threshold_prediction(
        self, node_id: str, known_labels: Dict[str, int], threshold: float = 0.5
    ) -> Optional[int]:
        score = self.neighbor_average(node_id, known_labels)
        return None if score is None else int(score >= threshold)
