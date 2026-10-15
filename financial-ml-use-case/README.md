# Trustworthy Machine Learning for Finance

This project records a bounded finance ML use case and plans its validation and implementation stages.

## Run the demonstration

```bash
python src/main.py
```

The demonstration prints `revise` because the material-segment validation slice is incomplete.

## Run tests

```bash
python -m pytest
```

The validation plan distinguishes later-period, segment, and stress evidence. It also requires controls to name an owner, trigger, and response. A stop condition takes precedence over revision; revision takes precedence over proceeding. These records organize review decisions but do not independently prove model quality.
