# NLP Suitability and Limits Assessment

This small standard-library Python project records whether an NLP proposal is ready for bounded evaluation.

It does not measure language understanding or model performance. It makes the proposal reviewable by requiring:

- an intended operational outcome;
- an input description;
- concrete ambiguity examples;
- evidence requirements;
- use-context risks;
- non-goals; and
- a human-review boundary.

## Run the example

```bash
cd nlp-limitations-assessment
PYTHONPATH=src python src/main.py
```

The complete example should recommend `proceed to bounded evaluation`.

## Run tests

```bash
cd nlp-limitations-assessment
python -m unittest discover -s tests -v
```

A proceed result means the proposal is structured for bounded evaluation. It is not approval for unrestricted production deployment.
