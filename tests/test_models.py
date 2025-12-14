"""Tests for generated Pydantic models."""

from datetime import datetime

import pytest
from pydantic import ValidationError

from opendirect21.models.generated import (
    Account,
    Address,
    Assignment,
    BookingstatusEnum,
    Contact,
    Creative,
    Line,
    Order,
    Organization,
    RatetypeEnum,
    StatusEnum,
)


def test_organization_model():
    """Test Organization model."""
    org = Organization(
        id="org-123",
        name="Test Publisher",
        status=StatusEnum.ACTIVE,
    )

    assert org.id == "org-123"
    assert org.name == "Test Publisher"
    assert org.status == StatusEnum.ACTIVE
    assert org.url is None  # Optional field


def test_organization_required_fields():
    """Test Organization required field validation."""
    # Missing required fields should raise ValidationError
    with pytest.raises(ValidationError) as exc_info:
        Organization(id="123")  # Missing name and status

    errors = exc_info.value.errors()
    assert len(errors) >= 2
    field_names = {e["loc"][0] for e in errors}
    assert "name" in field_names
    assert "status" in field_names


def test_account_model():
    """Test Account model."""
    account = Account(
        id="acc-456",
        buyerId="buyer-789",
        name="Test Account",
        status=StatusEnum.ACTIVE,
    )

    assert account.id == "acc-456"
    assert account.buyerId == "buyer-789"
    assert account.advertiserId is None  # Optional


def test_order_model():
    """Test Order model."""
    order = Order(
        id="order-001",
        accountId="acc-456",
        name="Q1 Campaign",
        startDate=datetime(2025, 1, 1),
        status=StatusEnum.ACTIVE,
    )

    assert order.id == "order-001"
    assert order.name == "Q1 Campaign"
    assert order.startDate.year == 2025
    assert order.endDate is None  # Optional


def test_line_model():
    """Test Line model."""
    line = Line(
        id="line-001",
        orderId="order-001",
        name="Display Line",
        bookingStatus=BookingstatusEnum.BOOKED,
        startDate=datetime(2025, 1, 1),
        rateType=RatetypeEnum.CPM,
    )

    assert line.id == "line-001"
    assert line.bookingStatus == BookingstatusEnum.BOOKED
    assert line.rateType == RatetypeEnum.CPM


def test_creative_model():
    """Test Creative model."""
    creative = Creative(
        id="creative-001",
        accountId="acc-456",
        name="Banner Creative",
        adFormatType="Display",  # Enum value as string
    )

    assert creative.id == "creative-001"
    assert creative.name == "Banner Creative"


def test_assignment_model():
    """Test Assignment model."""
    assignment = Assignment(
        id="assign-001",
        lineId="line-001",
        creativeId="creative-001",
        status=StatusEnum.ACTIVE,
    )

    assert assignment.id == "assign-001"
    assert assignment.lineId == "line-001"
    assert assignment.creativeId == "creative-001"


def test_contact_model():
    """Test Contact model."""
    contact = Contact(
        email="john@example.com",
        firstName="John",
        lastName="Doe",
        type="Technical",
    )

    assert contact.email == "john@example.com"
    assert contact.firstName == "John"
    assert contact.id is None  # Optional


def test_address_model():
    """Test Address model."""
    address = Address(
        street1="123 Main St",
        city="San Francisco",
        country="US",
    )

    assert address.street1 == "123 Main St"
    assert address.city == "San Francisco"
    assert address.country == "US"
    assert address.state is None  # Optional


def test_model_serialization():
    """Test model serialization to dict/JSON."""
    org = Organization(
        id="org-123",
        name="Test Publisher",
        status=StatusEnum.ACTIVE,
        url="https://example.com",
    )

    data = org.model_dump()
    assert isinstance(data, dict)
    assert data["id"] == "org-123"
    assert data["name"] == "Test Publisher"
    assert data["status"] == "Active"  # Enum serialized as string

    # Test JSON serialization
    json_str = org.model_dump_json()
    assert isinstance(json_str, str)
    assert "org-123" in json_str


def test_model_deserialization():
    """Test model deserialization from dict."""
    data = {
        "id": "org-456",
        "name": "Another Publisher",
        "status": "Inactive",
    }

    org = Organization(**data)
    assert org.id == "org-456"
    assert org.status == StatusEnum.INACTIVE


def test_enum_values():
    """Test enum values are correct."""
    assert StatusEnum.ACTIVE.value == "Active"
    assert StatusEnum.INACTIVE.value == "Inactive"
    assert StatusEnum.PENDING.value == "Pending"

    assert RatetypeEnum.CPM.value == "CPM"
    assert RatetypeEnum.CPC.value == "CPC"
    assert RatetypeEnum.CPA.value == "CPA"


def test_model_validation():
    """Test model field validation."""
    # Test with invalid status enum
    with pytest.raises(ValidationError):
        Organization(
            id="org-123",
            name="Test",
            status="InvalidStatus",  # Not a valid enum value
        )


def test_optional_fields():
    """Test optional fields work correctly."""
    order = Order(
        id="order-001",
        accountId="acc-456",
        name="Test Order",
        startDate=datetime(2025, 1, 1),
        status=StatusEnum.ACTIVE,
        # All other fields are optional
    )

    assert order.budget is None
    assert order.currency is None
    assert order.endDate is None
    assert order.providerData is None


def test_model_update():
    """Test updating model fields."""
    org = Organization(
        id="org-123",
        name="Original Name",
        status=StatusEnum.ACTIVE,
    )

    # Create new instance with updated fields
    org_data = org.model_dump()
    org_data["name"] = "Updated Name"
    updated_org = Organization(**org_data)

    assert updated_org.name == "Updated Name"
    assert updated_org.id == "org-123"


def test_model_with_nested_objects():
    """Test models with nested object references."""
    # Note: Address is referenced as string literal in Organization
    org = Organization(
        id="org-123",
        name="Test Org",
        status=StatusEnum.ACTIVE,
        address=None,  # Can set to None or an Address object
    )

    assert org.address is None

    # Can also create with address
    address = Address(
        street1="123 Main St",
        city="San Francisco",
        country="US",
    )

    org_with_address = Organization(
        id="org-456",
        name="Org with Address",
        status=StatusEnum.ACTIVE,
        address=address,
    )

    assert org_with_address.address is not None
    assert org_with_address.address.city == "San Francisco"
