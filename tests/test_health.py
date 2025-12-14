"""Tests for health check endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Test basic health check endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "service" in data
    assert "version" in data
    assert "timestamp" in data


@pytest.mark.asyncio
async def test_deep_health_check(client: AsyncClient):
    """Test deep health check endpoint."""
    response = await client.get("/health/deep")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "subsystems" in data
    assert data["subsystems"]["api"] == "operational"
    assert data["subsystems"]["storage"] == "operational"
    assert data["subsystems"]["models"] == "operational"


@pytest.mark.asyncio
async def test_service_info(client: AsyncClient):
    """Test service info endpoint."""
    response = await client.get("/info")
    assert response.status_code == 200
    data = response.json()
    assert "specifications" in data
    assert "opendirect" in data["specifications"]
    assert "adcom" in data["specifications"]
    assert data["specifications"]["opendirect"]["version"] == "2.1"
    assert data["specifications"]["adcom"]["version"] == "1.0"


@pytest.mark.asyncio
async def test_root_endpoint(client: AsyncClient):
    """Test root endpoint."""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert "version" in data
    assert "documentation" in data
    assert "specifications" in data
    assert "endpoints" in data
