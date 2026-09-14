# Contributing

Early-stage research scaffold. Keep benchmark ground truth read-only, prefer structured MCP operations, record tool versions/configuration, and do not claim security findings without reproducible evidence.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,eda]"
cp .env.example .env
pytest
```

For reproducible dependencies use `uv sync --frozen --extra dev --extra eda`.
See [Phase 1](docs/phase1.md) for Docker and endpoint acceptance tests.
