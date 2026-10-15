# Responsible Decision Feedback

A standard-library Python prototype for an explainable, challengeable review workflow.

## Run the demonstration

From this directory:

```bash
PYTHONPATH=src python src/main.py
```

## Run tests

From this directory:

```bash
PYTHONPATH=. python -m unittest discover -s tests
```

The workflow requires an explanation before a challenge, escalates challenges involving possible material harm or missing evidence, and records feedback only after a reviewer resolves the case.
