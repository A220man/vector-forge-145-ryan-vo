"""Recall API endpoint."""

from fastapi import APIRouter, HTTPException

from vector_forge.models.memory import VALID_BUDGETS, RecallRequest, RecallResponse
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
    if request.budget not in VALID_BUDGETS:
        raise HTTPException(
            status_code=400,
            detail=f"budget must be one of {sorted(VALID_BUDGETS)}, got {request.budget!r}",
        )
    return await memory_storage.recall(request)
