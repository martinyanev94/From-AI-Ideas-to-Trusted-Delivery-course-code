# Machine Learning and Operations Research Decision Model

This project compares predictive, optimization-based, and hybrid approaches for a constrained scheduling decision.

## Run the example

From the repository root:

```bash
python -m ml-operations-optimization.src.comparison
```

The expected teaching result is `optimization`. The comparison first requires feasibility, high fit, and high explainability, then ranks eligible approaches by on-time rate and total late minutes. The schedule values are illustrative; operational evaluation must use representative data and measures agreed with the people who use the schedule.

## Run tests

Install `pytest` in the project environment, then run:

```bash
python -m pytest ml-operations-optimization/tests
```
