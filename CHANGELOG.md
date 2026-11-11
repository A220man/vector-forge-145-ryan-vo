# Changelog

## 1.4.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.3.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

# Changelog

## [1.2.0] - 2026-11-08

### Added
- Hermes integration timestamp prefix feature (HERMES_RECALL_TIMESTAMP_PREFIX)
- Configurable timestamp prefix for auto-recall block and hindsight_recall tool
- Uses mentioned_at first, falls back to occurred_start
- Test coverage for timestamp formatting (tests/test_hermes_timestamp.py)

## [0.3.0] - 2026-11-05

### Added
- Hermes integration timestamp prefix feature (HERMES_RECALL_TIMESTAMP_PREFIX)
- Configurable timestamp prefix for auto-recall block and hindsight_recall tool
- Uses mentioned_at first, falls back to occurred_start
- Test coverage for timestamp formatting (tests/test_hermes_timestamp.py)

## [0.2.0] - 2026-10-31

### Added
- Memory models (MemoryItem, RetainRequest/Response, RecallRequest/Response/Result)
- In-memory thread-safe storage (MemoryStorage)
- Retain API endpoint (POST /v1/banks/{bank_id}/retain)
- Recall API endpoint (POST /v1/banks/{bank_id}/recall) with word-overlap ranking
- API router modules (retain.py, recall.py)
- Package init files for models, api, storage

## [0.1.0] - 2026-10-26

### Added
- Initial project structure
- FastAPI application skeleton
- Health check endpoint
- Basic test setup

