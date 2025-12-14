"""Tests for generated Adcom FastAPI routes."""

import pytest
from httpx import AsyncClient

from opendirect21.main import app
from opendirect21.models.generated.adcom import (
    Ad,
    Display,
    Banner,
    Video,
    Publisher,
)


@pytest.fixture
async def adcom_client() -> AsyncClient:
    """Create test client for Adcom routes."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_list_ads_empty(adcom_client: AsyncClient):
    """Test listing ads when none exist."""
    response = await adcom_client.get("/api/v1/adcom/ads")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_create_ad(adcom_client: AsyncClient):
    """Test creating an ad."""
    ad_data = {
        "id": "test-ad-001",
        "adomain": ["example.com"],
        "secure": 1,
    }

    response = await adcom_client.post("/api/v1/adcom/ads", json=ad_data)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == "test-ad-001"
    assert data["adomain"] == ["example.com"]


@pytest.mark.asyncio
async def test_get_ad(adcom_client: AsyncClient):
    """Test getting a specific ad."""
    # Create an ad first
    ad_data = {"id": "test-ad-002", "adomain": ["test.com"]}
    create_response = await adcom_client.post("/api/v1/adcom/ads", json=ad_data)
    assert create_response.status_code == 201

    # Get the ad
    response = await adcom_client.get("/api/v1/adcom/ads/test-ad-002")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "test-ad-002"


@pytest.mark.asyncio
async def test_get_ad_not_found(adcom_client: AsyncClient):
    """Test getting a non-existent ad."""
    response = await adcom_client.get("/api/v1/adcom/ads/nonexistent")
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


@pytest.mark.asyncio
async def test_update_ad(adcom_client: AsyncClient):
    """Test updating an ad."""
    # Create an ad
    ad_data = {"id": "test-ad-003", "secure": 0}
    await adcom_client.post("/api/v1/adcom/ads", json=ad_data)

    # Update the ad
    update_data = {"id": "test-ad-003", "secure": 1, "adomain": ["updated.com"]}
    response = await adcom_client.put("/api/v1/adcom/ads/test-ad-003", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["secure"] == 1
    assert data["adomain"] == ["updated.com"]


@pytest.mark.asyncio
async def test_delete_ad(adcom_client: AsyncClient):
    """Test deleting an ad."""
    # Create an ad
    ad_data = {"id": "test-ad-004"}
    await adcom_client.post("/api/v1/adcom/ads", json=ad_data)

    # Delete the ad
    response = await adcom_client.delete("/api/v1/adcom/ads/test-ad-004")
    assert response.status_code == 204

    # Verify it's gone
    get_response = await adcom_client.get("/api/v1/adcom/ads/test-ad-004")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_list_ads_with_pagination(adcom_client: AsyncClient):
    """Test listing ads with pagination."""
    # Create multiple ads
    for i in range(5):
        ad_data = {"id": f"ad-page-{i}"}
        await adcom_client.post("/api/v1/adcom/ads", json=ad_data)

    # Get first page
    response = await adcom_client.get("/api/v1/adcom/ads?skip=0&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    # Get second page
    response = await adcom_client.get("/api/v1/adcom/ads?skip=2&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@pytest.mark.asyncio
async def test_create_display(adcom_client: AsyncClient):
    """Test creating a display ad."""
    display_data = {
        "mime": "text/html",
        "w": 300,
        "h": 250,
        "api": [1, 2],
    }

    response = await adcom_client.post("/api/v1/adcom/displays", json=display_data)
    assert response.status_code == 201
    data = response.json()
    assert data["mime"] == "text/html"
    assert data["w"] == 300
    assert data["h"] == 250


@pytest.mark.asyncio
async def test_create_banner(adcom_client: AsyncClient):
    """Test creating a banner."""
    banner_data = {
        "img": "https://example.com/banner.jpg",
        "w": 728,
        "h": 90,
    }

    response = await adcom_client.post("/api/v1/adcom/banners", json=banner_data)
    assert response.status_code == 201
    data = response.json()
    assert data["img"] == "https://example.com/banner.jpg"


@pytest.mark.asyncio
async def test_create_video(adcom_client: AsyncClient):
    """Test creating a video ad."""
    video_data = {
        "mime": ["video/mp4"],
        "w": 640,
        "h": 480,
        "maxdur": 30,
    }

    response = await adcom_client.post("/api/v1/adcom/videos", json=video_data)
    assert response.status_code == 201
    data = response.json()
    assert data["mime"] == ["video/mp4"]
    assert data["maxdur"] == 30


@pytest.mark.asyncio
async def test_create_publisher(adcom_client: AsyncClient):
    """Test creating a publisher."""
    publisher_data = {
        "id": "pub-001",
        "name": "Test Publisher",
        "domain": "publisher.com",
    }

    response = await adcom_client.post("/api/v1/adcom/publishers", json=publisher_data)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == "pub-001"
    assert data["name"] == "Test Publisher"


@pytest.mark.asyncio
async def test_list_all_media_types(adcom_client: AsyncClient):
    """Test that all media type endpoints exist."""
    endpoints = [
        "/api/v1/adcom/ads",
        "/api/v1/adcom/displays",
        "/api/v1/adcom/banners",
        "/api/v1/adcom/videos",
        "/api/v1/adcom/audios",
        "/api/v1/adcom/natives",
    ]

    for endpoint in endpoints:
        response = await adcom_client.get(endpoint)
        assert response.status_code == 200, f"Endpoint {endpoint} failed"


@pytest.mark.asyncio
async def test_list_all_asset_types(adcom_client: AsyncClient):
    """Test that all asset type endpoints exist."""
    endpoints = [
        "/api/v1/adcom/assets",
        "/api/v1/adcom/linkassets",
        "/api/v1/adcom/imageassets",
        "/api/v1/adcom/videoassets",
        "/api/v1/adcom/titleassets",
        "/api/v1/adcom/dataassets",
        "/api/v1/adcom/events",
    ]

    for endpoint in endpoints:
        response = await adcom_client.get(endpoint)
        assert response.status_code == 200, f"Endpoint {endpoint} failed"


@pytest.mark.asyncio
async def test_list_all_context_types(adcom_client: AsyncClient):
    """Test that all context type endpoints exist."""
    endpoints = [
        "/api/v1/adcom/publishers",
        "/api/v1/adcom/contents",
        "/api/v1/adcom/users",
        "/api/v1/adcom/devices",
        "/api/v1/adcom/geos",
    ]

    for endpoint in endpoints:
        response = await adcom_client.get(endpoint)
        assert response.status_code == 200, f"Endpoint {endpoint} failed"


@pytest.mark.asyncio
async def test_validation_error_missing_required_field(adcom_client: AsyncClient):
    """Test validation error when required field is missing."""
    # Display requires 'mime' field
    display_data = {"w": 300, "h": 250}

    response = await adcom_client.post("/api/v1/adcom/displays", json=display_data)
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_pagination_limits(adcom_client: AsyncClient):
    """Test pagination parameter validation."""
    # Test negative skip
    response = await adcom_client.get("/api/v1/adcom/ads?skip=-1")
    assert response.status_code == 422

    # Test limit exceeding max
    response = await adcom_client.get("/api/v1/adcom/ads?limit=2000")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_root_endpoint_shows_adcom(adcom_client: AsyncClient):
    """Test that root endpoint mentions adcom."""
    response = await adcom_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "adcom" in data["endpoints"]
    assert data["endpoints"]["adcom"] == "/api/v1/adcom"


@pytest.mark.asyncio
async def test_full_crud_cycle(adcom_client: AsyncClient):
    """Test complete CRUD cycle for an ad."""
    # Create
    ad_data = {"id": "full-cycle-ad", "adomain": ["cycle.com"]}
    create_response = await adcom_client.post("/api/v1/adcom/ads", json=ad_data)
    assert create_response.status_code == 201

    # Read
    read_response = await adcom_client.get("/api/v1/adcom/ads/full-cycle-ad")
    assert read_response.status_code == 200

    # Update
    update_data = {"id": "full-cycle-ad", "adomain": ["updated-cycle.com"], "secure": 1}
    update_response = await adcom_client.put(
        "/api/v1/adcom/ads/full-cycle-ad", json=update_data
    )
    assert update_response.status_code == 200
    assert update_response.json()["secure"] == 1

    # List (should include our ad)
    list_response = await adcom_client.get("/api/v1/adcom/ads")
    assert list_response.status_code == 200
    ids = [ad["id"] for ad in list_response.json()]
    assert "full-cycle-ad" in ids

    # Delete
    delete_response = await adcom_client.delete("/api/v1/adcom/ads/full-cycle-ad")
    assert delete_response.status_code == 204

    # Verify deletion
    verify_response = await adcom_client.get("/api/v1/adcom/ads/full-cycle-ad")
    assert verify_response.status_code == 404
