"""Integration tests for the /api/v1/analysis/variance endpoint."""
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


async def test_variance_happy_path(client: AsyncClient) -> None:
    """POST with valid fiscal_period returns 200 with expected fields."""
    response = await client.post(
        "/api/v1/analysis/variance", json={"fiscal_period": "2024-Q4"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["fiscal_period"] == "2024-Q4"
    assert data["status"] == "queued"


async def test_variance_with_department(client: AsyncClient) -> None:
    """POST with optional department field returns 200 and echoes the field."""
    response = await client.post(
        "/api/v1/analysis/variance",
        json={"fiscal_period": "2024-Q4", "department": "Engineering"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["fiscal_period"] == "2024-Q4"
    assert data["department"] == "Engineering"
    assert data["status"] == "queued"


async def test_variance_missing_required_field(client: AsyncClient) -> None:
    """POST without fiscal_period returns 422 Unprocessable Entity."""
    response = await client.post(
        "/api/v1/analysis/variance", json={"department": "Finance"}
    )
    assert response.status_code == 422
