# Graph ML Prototype

This project evaluates a small graph application for predicting whether a support case requires escalation.

## Run the demonstration

From this directory:

```bash
python src/main.py
```

The demonstration computes a neighbor-average score for `case_101` while withholding its own label, then prints an evaluation brief.

## Run tests

From the repository root:

```bash
python -m unittest discover -s graph-ml-prototype/tests
```

The prototype is intentionally transparent. It does not establish production readiness. A real evaluation must use prediction-time data, inspect leakage through both node fields and relationships, compare against a case-attribute baseline, and test whether neighboring cases actually share outcomes.
