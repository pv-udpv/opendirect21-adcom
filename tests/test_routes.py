"""Tests for generated API routes."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from opendirect21.api.generated import router
from opendirect21.store import get_store


@pytest.fixture
def app():
    """Create FastAPI app with routes."""
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_store():
    """Reset store before each test."""
    # Clear the global store
    store = get_store()
    store.data = {}
    yield
    store.data = {}


def test_list_organizations_empty(client):
    """Test listing organizations when none exist."""
    response = client.get("/api/v1/organizations")
    assert response.status_code == 200
    assert response.json() == []


def test_create_organization(client):
    """Test creating an organization."""
    org_data = {
        "id": "org-123",
        "name": "Test Publisher",
        "status": "Active",
    }

    response = client.post("/api/v1/organizations", json=org_data)
    assert response.status_code == 201

    data = response.json()
    assert data["id"] == "org-123"
    assert data["name"] == "Test Publisher"
    assert data["status"] == "Active"


def test_get_organization_by_id(client):
    """Test getting an organization by ID."""
    # Create first
    org_data = {
        "id": "org-456",
        "name": "Another Publisher",
        "status": "Active",
    }
    client.post("/api/v1/organizations", json=org_data)

    # Get by ID
    response = client.get("/api/v1/organizations/org-456")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == "org-456"
    assert data["name"] == "Another Publisher"


def test_get_organization_not_found(client):
    """Test getting non-existent organization returns 404."""
    response = client.get("/api/v1/organizations/nonexistent")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_organization(client):
    """Test updating an organization."""
    # Create first
    org_data = {
        "id": "org-789",
        "name": "Original Name",
        "status": "Active",
    }
    client.post("/api/v1/organizations", json=org_data)

    # Update
    updated_data = {
        "id": "org-789",
        "name": "Updated Name",
        "status": "Inactive",
    }
    response = client.put("/api/v1/organizations/org-789", json=updated_data)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["status"] == "Inactive"


def test_update_organization_not_found(client):
    """Test updating non-existent organization returns 404."""
    org_data = {
        "id": "org-999",
        "name": "Test",
        "status": "Active",
    }
    response = client.put("/api/v1/organizations/nonexistent", json=org_data)
    assert response.status_code == 404


def test_delete_organization(client):
    """Test deleting an organization."""
    # Create first
    org_data = {
        "id": "org-delete",
        "name": "To Delete",
        "status": "Active",
    }
    client.post("/api/v1/organizations", json=org_data)

    # Delete
    response = client.delete("/api/v1/organizations/org-delete")
    assert response.status_code == 204

    # Verify deleted
    get_response = client.get("/api/v1/organizations/org-delete")
    assert get_response.status_code == 404


def test_delete_organization_not_found(client):
    """Test deleting non-existent organization returns 404."""
    response = client.delete("/api/v1/organizations/nonexistent")
    assert response.status_code == 404


def test_list_organizations_pagination(client):
    """Test pagination in list endpoint."""
    # Create 10 organizations
    for i in range(10):
        org_data = {
            "id": f"org-{i}",
            "name": f"Organization {i}",
            "status": "Active",
        }
        client.post("/api/v1/organizations", json=org_data)

    # Get first page
    response = client.get("/api/v1/organizations?skip=0&limit=3")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

    # Get second page
    response = client.get("/api/v1/organizations?skip=3&limit=3")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

    # Get last page
    response = client.get("/api/v1/organizations?skip=9&limit=3")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1


def test_accounts_crud(client):
    """Test CRUD operations for accounts."""
    # Create
    account_data = {
        "id": "acc-123",
        "buyerId": "buyer-456",
        "name": "Test Account",
        "status": "Active",
    }
    response = client.post("/api/v1/accounts", json=account_data)
    assert response.status_code == 201

    # List
    response = client.get("/api/v1/accounts")
    assert response.status_code == 200
    assert len(response.json()) == 1

    # Get
    response = client.get("/api/v1/accounts/acc-123")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Account"

    # Update
    updated_data = {
        **account_data,
        "name": "Updated Account",
    }
    response = client.put("/api/v1/accounts/acc-123", json=updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Account"

    # Delete
    response = client.delete("/api/v1/accounts/acc-123")
    assert response.status_code == 204


def test_orders_crud(client):
    """Test CRUD operations for orders."""
    order_data = {
        "id": "order-001",
        "accountId": "acc-456",
        "name": "Q1 Campaign",
        "startDate": "2025-01-01T00:00:00",
        "status": "Active",
    }

    response = client.post("/api/v1/orders", json=order_data)
    assert response.status_code == 201
    assert response.json()["name"] == "Q1 Campaign"

    response = client.get("/api/v1/orders/order-001")
    assert response.status_code == 200


def test_lines_crud(client):
    """Test CRUD operations for lines."""
    line_data = {
        "id": "line-001",
        "orderId": "order-001",
        "name": "Display Line",
        "bookingStatus": "Booked",
        "startDate": "2025-01-01T00:00:00",
        "rateType": "CPM",
    }

    response = client.post("/api/v1/lines", json=line_data)
    assert response.status_code == 201
    assert response.json()["bookingStatus"] == "Booked"


def test_creatives_crud(client):
    """Test CRUD operations for creatives."""
    creative_data = {
        "id": "creative-001",
        "accountId": "acc-456",
        "name": "Banner Creative",
        "adFormatType": "Display",
    }

    response = client.post("/api/v1/creatives", json=creative_data)
    assert response.status_code == 201
    assert response.json()["adFormatType"] == "Display"


def test_invalid_pagination_params(client):
    """Test invalid pagination parameters."""
    # Negative skip
    response = client.get("/api/v1/organizations?skip=-1")
    assert response.status_code == 422  # Validation error

    # Limit too large
    response = client.get("/api/v1/organizations?limit=10000")
    assert response.status_code == 422


def test_create_with_missing_required_fields(client):
    """Test creating object with missing required fields."""
    incomplete_org = {
        "id": "org-incomplete",
        # Missing name and status
    }

    response = client.post("/api/v1/organizations", json=incomplete_org)
    assert response.status_code == 422  # Validation error


def test_multiple_endpoints_exist(client):
    """Test that all expected endpoints exist."""
    # Check a few key endpoints
    endpoints = [
        "/api/v1/organizations",
        "/api/v1/accounts",
        "/api/v1/orders",
        "/api/v1/lines",
        "/api/v1/creatives",
        "/api/v1/assignments",
        "/api/v1/products",
        "/api/v1/contacts",
    ]

    for endpoint in endpoints:
        response = client.get(endpoint)
        # Should return 200 (empty list) or other valid status, not 404
        assert response.status_code != 404


def test_route_count(app):
    """Test that expected number of routes exist."""
    # Should have 105 routes (21 objects × 5 operations each)
    route_count = len(app.routes)
    # Account for the default 404 and 500 routes
    assert route_count >= 105
