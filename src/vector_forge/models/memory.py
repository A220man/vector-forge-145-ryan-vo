
"""Memory models for Hindsight API."""

from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class MemoryItem(BaseModel):
    """A single memory item."""

    id: UUID = Field(default_factory=uuid4)
    text: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    mentioned_at: datetime | None = None
    occurred_start: datetime | None = None
    occurred_end: datetime | None = None
    tags: list[str] = Field(default_factory=list)
    bank_id: str | None = None


class RetainRequest(BaseModel):
    """Request to retain memories."""

    items: list[MemoryItem]
    bank_id: str
    update_mode: str = "append"


class RetainResponse(BaseModel):
    """Response from retain operation."""

    operation_id: UUID
    status: str = "accepted"
    accepted_count: int


class RecallRequest(BaseModel):
    """Request to recall memories."""

    query: str
    budget: str = "medium"
    bank_id: str
    limit: int = 10


class RecallResult(BaseModel):
    """A single recall result with score."""

    item: MemoryItem
    score: float


class RecallResponse(BaseModel):
    """Response from recall operation."""

    results: list[RecallResult]
    query: str
