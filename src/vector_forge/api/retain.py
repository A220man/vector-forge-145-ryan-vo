"""Retain API endpoint."""

from fastapi import APIRouter, HTTPException
from uuid import UUID

from vector_forge.models.memory import RetainRequest, RetainResponse
from vector_forge.storage.memory import memory_storage

router = APIRouter(prefix="/v1/banks", tags=["retain"])


@router.post("/{bank_id}/retain", response_model=RetainResponse)
async def retain_memories(bank_id: str, request: RetainRequest):
    """Store memory items in a bank."""
    if request.bank_id != bank_id:
        raise HTTPException(
            status_code=400,
            detail="bank_id in path must match bank_id in request body",
        )
    return await memory_storage.retain(request)
