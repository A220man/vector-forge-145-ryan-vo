"""Tests for recall endpoint."""
import pytest
from httpx import ASGITransport, AsyncClient

from vector_forge.main import app


@pytest.mark.asyncio
async def test_recall_memories():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # First, retain some memories
        await client.post(
            "/v1/banks/test-bank/retain",
            json={
                "bank_id": "test-bank",
                "items": [
                    {"text": "User prefers dark mode", "tags": ["preference", "ui"]},
                    {"text": "User works in timezone UTC-5", "tags": ["timezone"]},
                    {"text": "User likes Python", "tags": ["language"]},
                ],
            },
        )

        # Now recall with a query
        response = await client.post(
            "/v1/banks/test-bank/recall",
            json={
                "bank_id": "test-bank",
                "query": "user prefers dark",
                "budget": "medium",
                "limit": 10,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["query"] == "user prefers dark"
        assert len(data["results"]) >= 1
        # First result should be about dark mode
        assert "dark" in data["results"][0]["item"]["text"].lower()
        # Score should be > 0
        assert data["results"][0]["score"] > 0


@pytest.mark.asyncio
async def test_recall_empty_bank():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/v1/banks/empty-bank/recall",
            json={
                "bank_id": "empty-bank",
                "query": "anything",
                "budget": "low",
                "limit": 5,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["results"] == []
        assert data["query"] == "anything"


@pytest.mark.asyncio
async def test_recall_bank_id_mismatch():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/v1/banks/bank-a/recall",
            json={
                "bank_id": "bank-b",
                "query": "test",
            },
        )
        assert response.status_code == 400
        assert "bank_id in path must match" in response.json()["detail"]


@pytest.mark.asyncio
async def test_recall_empty_query_returns_no_results():
    """An empty/whitespace query matches nothing (no score-0 false positives)."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post(
            "/v1/banks/empty-query-bank/retain",
            json={
                "bank_id": "empty-query-bank",
                "items": [{"text": "User prefers dark mode"}],
            },
        )
        for query in ("", "   ", "\t\n"):
            response = await client.post(
                "/v1/banks/empty-query-bank/recall",
                json={"bank_id": "empty-query-bank", "query": query, "limit": 10},
            )
            assert response.status_code == 200
            data = response.json()
            assert data["results"] == [], f"query {query!r} should match nothing"
            assert data["query"] == query


@pytest.mark.asyncio
async def test_recall_invalid_budget_returns_400():
    """A budget outside low/medium/high is rejected with 400."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post(
            "/v1/banks/budget-bank/retain",
            json={"bank_id": "budget-bank", "items": [{"text": "anything"}]},
        )
        response = await client.post(
            "/v1/banks/budget-bank/recall",
            json={"bank_id": "budget-bank", "query": "anything", "budget": "ultra"},
        )
        assert response.status_code == 400
        assert "budget must be one of" in response.json()["detail"]


@pytest.mark.asyncio
async def test_recall_valid_budgets_accepted():
    """low, medium and high budgets are all accepted."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post(
            "/v1/banks/budget-ok-bank/retain",
            json={"bank_id": "budget-ok-bank", "items": [{"text": "budget check"}]},
        )
        for budget in ("low", "medium", "high"):
            response = await client.post(
                "/v1/banks/budget-ok-bank/recall",
                json={"bank_id": "budget-ok-bank", "query": "budget check", "budget": budget},
            )
            assert response.status_code == 200, f"budget {budget} should be accepted"
