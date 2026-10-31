"""Main FastAPI application for Vector Forge Hindsight."""

from fastapi import FastAPI

from vector_forge.api.retain import router as retain_router
from vector_forge.api.recall import router as recall_router

app = FastAPI(
    title="Vector Forge Hindsight",
    description="Agent Memory That Learns",
    version="0.1.0",
)

app.include_router(retain_router)
app.include_router(recall_router)


@app.get("/healthz")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}
