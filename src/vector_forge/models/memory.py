"""Memory models for Hindsight API."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class MemoryItem(BaseModel):
    """A single memory item."""

    id: UUID = Field(default_factory=uuid4)
    text: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    mentioned_at: Optional[datetime] = None
    occurred_start: Optional[datetime] = None
    occurred_end: Optional[datetime] = None
    tags: List[str] = Field(default_factory=list)
    bank_id: str


class RetainRequest(BaseModel):
    """Request to retain memories."""

    items: List[MemoryItem]
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

    results: List[RecallResult]
    query: str
