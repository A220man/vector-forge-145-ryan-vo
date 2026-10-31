# Changelog

## 1.1.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.0.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-10-26

### Added
- Initial project structure
- FastAPI application skeleton
- Health check endpoint
- Basic test setup

## [0.2.0] - 2026-10-31

### Added
- Memory models (MemoryItem, RetainRequest/Response, RecallRequest/Response/Result)
- In-memory thread-safe storage (MemoryStorage)
- Retain API endpoint (POST /v1/banks/{bank_id}/retain)
- Recall API endpoint (POST /v1/banks/{bank_id}/recall) with word-overlap ranking
- API router modules (retain.py, recall.py)
- Package init files for models, api, storage
