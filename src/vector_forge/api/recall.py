"""Recall API endpoint."""

from fastapi import APIRouter, HTTPException

from vector_forge.models.memory import RecallRequest, RecallResponse
from vector_forge.storage.memory import memory_storage

router = APIRouter(prefix="/v1/banks", tags=["recall"])


@router.post("/{bank_id}/recall", response_model=RecallResponse)
async def recall_memories(bank_id: str, request: RecallRequest):
    """Recall memories from a bank matching the query."""
    if request.bank_id != bank_id:
        raise HTTPException(
            status_code=400,
            detail="bank_id in path must match bank_id in request body",
        )
    return await memory_storage.recall(request)
