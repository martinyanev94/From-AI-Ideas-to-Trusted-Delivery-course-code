# Explainability and Trust Review

This project creates an explainability requirements matrix for an illustrative high-stakes decision. It matches stakeholder-specific explanations and review depth, then checks whether each row has an owner, human check, escalation path, correction action, and resolved control state.

Run from the project directory with:

```bash
PYTHONPATH=. python src/main.py
```

Run tests with:

```bash
pytest tests
```

The report returns `proceed` only when explanation requirements match each stakeholder role, review depth is proportionate to the stakes, and accountability controls are present and resolved. The rule is a review aid, not proof that an AI system is safe or lawful.
