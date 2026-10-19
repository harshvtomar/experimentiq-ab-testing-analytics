# Local data lifecycle
`python -m src.pipeline` downloads the original checksum-pinned CSV into `data/raw/hillstrom.csv` with a provenance sidecar, then creates `data/processed/customers.csv` and `data/processed/experimentiq.sqlite`.

Raw bytes are immutable: mismatches fail instead of overwriting. Every original field is retained. No rows are removed. Generated customer-level files are ignored by Git because redistribution permission was not established. Public reports and dashboard downloads contain aggregates only. See `docs/DATA_SOURCE.md`.
