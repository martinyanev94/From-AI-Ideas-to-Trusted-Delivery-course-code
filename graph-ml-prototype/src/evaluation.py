from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass(frozen=True)
class GraphApplicationBrief:
    task: str
    prediction_time: str
    data_requirements: List[str]
    leakage_risks: List[str]
    limitations: List[str]
    baseline: str
    recommendation: str

    def validate(self) -> None:
        required = [self.task, self.prediction_time, self.baseline, self.recommendation]
        if any(not value.strip() for value in required):
            raise ValueError("task, time, baseline, and recommendation are required")
        if not self.data_requirements or not self.leakage_risks or not self.limitations:
            raise ValueError("evaluation evidence is incomplete")

    def as_record(self) -> Dict[str, Any]:
        self.validate()
        return {
            "task": self.task,
            "prediction_time": self.prediction_time,
            "data_requirements": self.data_requirements,
            "leakage_risks": self.leakage_risks,
            "limitations": self.limitations,
            "baseline": self.baseline,
            "recommendation": self.recommendation,
        }
