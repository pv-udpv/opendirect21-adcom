"""Pytest configuration and fixtures."""

import pytest
from httpx import AsyncClient

from opendirect21.main import app
from opendirect21.store import InMemoryStore


@pytest.fixture
async def client() -> AsyncClient:
    """Create test client."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def store() -> InMemoryStore:
    """Create test data store."""
    return InMemoryStore()
