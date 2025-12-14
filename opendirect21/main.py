"""FastAPI application entry point.

Starts the OpenDirect 2.1 + Adcom v1.0 reference server with all routes and configuration.
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from opendirect21.config import get_settings
from opendirect21.store import InMemoryStore
from opendirect21.api.health import router as health_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Global data store (can be replaced with database)
data_store = InMemoryStore()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application startup and shutdown."""
    # Startup
    logger.info("🚀 Starting OpenDirect 2.1 + Adcom v1.0 Server")
    logger.info(f"📡 API Documentation: http://localhost:8000/docs")
    logger.info(f"📚 Alternative Docs: http://localhost:8000/redoc")

    yield

    # Shutdown
    logger.info("🛑 Shutting down server")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title="OpenDirect 2.1 + Adcom v1.0 API",
        description="REST API for Programmatic Media Trading with auto-generated models from IAB specifications",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )

    # Include routers
    app.include_router(health_router, tags=["health"])

    # Root endpoint
    @app.get("/", tags=["root"])
    async def root():
        """API root endpoint with metadata."""
        return {
            "service": "OpenDirect 2.1 + Adcom v1.0 Reference Server",
            "version": "0.1.0",
            "documentation": "/docs",
            "specifications": {
                "opendirect": "2.1 Final",
                "adcom": "1.0 Final",
            },
            "endpoints": {
                "health": "/health",
                "health_deep": "/health/deep",
                "info": "/info",
                "docs": "/docs",
                "redoc": "/redoc",
            },
        }

    # Error handlers
    @app.exception_handler(404)
    async def not_found_handler(request, exc):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Endpoint not found", "path": request.url.path},
        )

    @app.exception_handler(500)
    async def internal_error_handler(request, exc):
        logger.error(f"Internal server error: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"},
        )

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        app,
        host=settings.server_host,
        port=settings.server_port,
        reload=settings.server_reload,
        log_level=settings.log_level.lower(),
    )
