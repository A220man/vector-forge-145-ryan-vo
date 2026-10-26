# Vector Forge 145 - Hindsight

> Work in progress. This checkpoint may be incomplete or fail tests. See PLAN.md and STATUS.md before use.


Agent Memory That Learns

## Quick Start

```bash
pip install -e ".[dev]"
uvicorn vector_forge.main:app --reload
curl http://localhost:8000/healthz
```

## API Endpoints

- GET /healthz - Health check
- POST /v1/banks/{bank_id}/retain - Store memories
- POST /v1/banks/{bank_id}/recall - Query memories

## Development

```bash
pytest
ruff check .
```

## License

MIT

Maintainer: Ryan Vo <ryandtvo@gmail.com>
