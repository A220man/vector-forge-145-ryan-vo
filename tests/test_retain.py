"""Tests for retain endpoint."""
import pytest
from httpx import AsyncClient, ASGITransport
from uuid import UUID
from vector_forge.main import app


@pytest.mark.asyncio
async def test_retain_memories():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/v1/banks/test-bank/retain",
            json={
                "bank_id": "test-bank",
                "items": [
                    {
                        "text": "User prefers dark mode",
                        "metadata": {"source": "chat"},
                        "tags": ["preference", "ui"],
                    },
                    {
                        "text": "User works in timezone UTC-5",
                        "metadata": {"source": "profile"},
                        "tags": ["timezone"],
                    },
                ],
                "update_mode": "append",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "accepted"
        assert data["accepted_count"] == 2
        # Verify operation_id is a valid UUID
        UUID(data["operation_id"])


@pytest.mark.asyncio
async def test_retain_bank_id_mismatch():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/v1/banks/bank-a/retain",
            json={
                "bank_id": "bank-b",
                "items": [{"text": "test"}],
            },
        )
        assert response.status_code == 400
        assert "bank_id in path must match" in response.json()["detail"]
