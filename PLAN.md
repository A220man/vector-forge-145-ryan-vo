# Product development plan

Each round completes one feature or repair. Future items are planned, not implemented claims.

## Current round

core-api-skeleton

## Roadmap

### core-api-skeleton — Core API Skeleton with Health Check

Status: in_progress

Acceptance:
- FastAPI application starts and responds to GET /healthz
- Basic project structure with pyproject.toml, README.md, CHANGELOG.md
- Unit test for health endpoint passes

Implementation: `src/vector_forge/main.py`, `src/vector_forge/__init__.py`, `pyproject.toml`, `README.md`, `CHANGELOG.md`, `tests/test_health.py`

Tests: `tests/test_health.py`

### memory-retain-endpoint — Memory Retain Endpoint

Status: planned

Acceptance:
- POST /v1/banks/{bank_id}/retain accepts JSON payload
- Returns operation ID and status
- Persists memory items with timestamps

Implementation: `src/vector_forge/api/retain.py`, `src/vector_forge/models/memory.py`, `src/vector_forge/storage/memory.py`

Tests: `tests/test_retain.py`

### memory-recall-endpoint — Memory Recall Endpoint

Status: planned

Acceptance:
- POST /v1/banks/{bank_id}/recall accepts query and returns memories
- Supports budget parameter (low/medium/high)
- Returns ranked results with scores

Implementation: `src/vector_forge/api/recall.py`, `src/vector_forge/services/recall.py`

Tests: `tests/test_recall.py`

### hermes-integration-timestamp — Hermes Integration: Timestamp Prefix in Recall Injection

Status: planned

Acceptance:
- Configuration option recall_timestamp_prefix (default off)
- Auto-recall block prefixes memories with [YYYY-MM-DD]
- hindsight_recall tool prefixes memories with [YYYY-MM-DD]
- Uses mentioned_at first, falls back to occurred_start

Implementation: `src/vector_forge/integrations/hermes/__init__.py`, `src/vector_forge/integrations/hermes/config.py`

Tests: `tests/test_hermes_timestamp.py`

