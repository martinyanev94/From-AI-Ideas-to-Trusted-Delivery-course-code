# Portfolio review dashboard

This standard-library Python CLI loads structured project records and renders value, readiness, provenance, ethical risk, ownership, next decision, and evidence status.

Run from this directory:

```bash
PYTHONPATH=src python src/main.py --input data/portfolio.json
python -m pytest tests
```

The dashboard organizes review evidence; it does not independently prove data quality, business value, or ethical acceptability.
