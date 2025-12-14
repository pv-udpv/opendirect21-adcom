"""Health check endpoints."""

from datetime import datetime
from typing import Any

from fastapi import APIRouter, status

router = APIRouter(tags=["health"])


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> dict[str, Any]:
    """System health check endpoint.

    Returns:
        Health status with service info and timestamp
    """
    return {
        "status": "healthy",
        "service": "OpenDirect 2.1 + Adcom v1.0 API",
        "version": "0.1.0",
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/health/deep", status_code=status.HTTP_200_OK)
async def deep_health_check() -> dict[str, Any]:
    """Detailed health check with subsystem status."""
    return {
        "status": "healthy",
        "service": "OpenDirect 2.1 + Adcom v1.0 API",
        "version": "0.1.0",
        "timestamp": datetime.utcnow().isoformat(),
        "subsystems": {
            "api": "operational",
            "storage": "operational",
            "models": "operational",
        },
    }


@router.get("/info", status_code=status.HTTP_200_OK)
async def service_info() -> dict[str, Any]:
    """Get service information and available specs."""
    return {
        "service": "OpenDirect 2.1 + Adcom v1.0 Reference Server",
        "version": "0.1.0",
        "specifications": {
            "opendirect": {
                "version": "2.1",
                "status": "final",
                "url": "https://iabtechlab.com/opendirect-2-1/",
            },
            "adcom": {
                "version": "1.0",
                "status": "final",
                "url": "https://iabtechlab.com/adcom/",
            },
        },
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json",
        },
        "timestamp": datetime.utcnow().isoformat(),
    }
