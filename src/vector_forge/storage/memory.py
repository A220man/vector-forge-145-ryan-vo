"""In-memory storage for memory items."""

import asyncio
from typing import Dict, List
from uuid import UUID, uuid4

from vector_forge.models.memory import (
    MemoryItem,
    RecallRequest,
    RecallResponse,
    RecallResult,
    RetainRequest,
    RetainResponse,
)


class MemoryStorage:
    """Thread-safe in-memory storage for memory items."""

    def __init__(self):
        self._banks: Dict[str, Dict[UUID, MemoryItem]] = {}
        self._lock = asyncio.Lock()

    async def retain(self, request: RetainRequest) -> RetainResponse:
        """Store memory items."""
        async with self._lock:
            bank = self._banks.setdefault(request.bank_id, {})
            for item in request.items:
                item.bank_id = request.bank_id
                bank[item.id] = item
            return RetainResponse(
                operation_id=uuid4(),
                status="accepted",
                accepted_count=len(request.items),
            )

    async def recall(self, request: RecallRequest) -> RecallResponse:
        """Recall memories matching query."""
        async with self._lock:
            bank = self._banks.get(request.bank_id, {})
            results = []
            query_words = set(request.query.lower().split())
            for item in bank.values():
                text_words = set(item.text.lower().split())
                if not query_words:
                    score = 0.0
                else:
                    overlap = len(query_words & text_words)
                    score = overlap / len(query_words)
                if score > 0:
                    results.append(RecallResult(item=item, score=score))

            results.sort(key=lambda r: r.score, reverse=True)
            return RecallResponse(
                results=results[:request.limit],
                query=request.query,
            )

    async def get_bank_stats(self, bank_id: str) -> Dict:
        """Get statistics for a bank."""
        async with self._lock:
            count = len(self._banks.get(bank_id, {}))
            return {"bank_id": bank_id, "memory_count": count}


memory_storage = MemoryStorage()
