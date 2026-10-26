"""Main FastAPI application for Vector Forge Hindsight."""

from fastapi import FastAPI

app = FastAPI(
    title="Vector Forge Hindsight",
    description="Agent Memory That Learns",
    version="0.1.0",
)


@app.get("/healthz")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}
