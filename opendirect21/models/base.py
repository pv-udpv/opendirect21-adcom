"""Base model classes and utilities."""

from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class TimestampedModel(BaseModel):
    """Base model with timestamp fields."""

    model_config = ConfigDict(from_attributes=True)

    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, description="Last update timestamp"
    )


class IDModel(BaseModel):
    """Base model with ID field."""

    model_config = ConfigDict(from_attributes=True)

    id: str = Field(default_factory=lambda: str(uuid4()), description="Unique identifier (UUID)")


class BaseEntity(IDModel, TimestampedModel):
    """Base entity with ID and timestamps."""

    model_config = ConfigDict(from_attributes=True)


class BaseResponse(BaseModel):
    """Base response model."""

    model_config = ConfigDict(from_attributes=True)
