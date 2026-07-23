"""Unit tests for the /health endpoint in src/main.py."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from src.main import app


@pytest.fixture()
async def client() -> AsyncClient:  # type: ignore[override]
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as ac:
        yield ac


async def test_health_returns_200(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200


async def test_health_status_ok(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.json()["status"] == "ok"


async def test_health_version_present(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert "version" in response.json()
