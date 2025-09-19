"""
Application entrypoint for Core User Service.
Initializes FastAPI app, CORS, health/ready endpoints, and API routers.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.users import router as users_router
from app.core.settings import settings


def _compute_cors_origins() -> list[str]:
    """
    Compute allowed CORS origins from settings.

    - Converts settings.cors_origins (List[AnyHttpUrl] | List[str]) into list[str].
    - If environment is "dev" and no origins are configured, returns ["*"].
    """
    raw: list[str] = [str(o) for o in settings.cors_origins] if settings.cors_origins else []
    if settings.env.lower() == "dev" and not raw:
        return ["*"]
    return raw


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Includes:
    - Service metadata (title, version)
    - CORS middleware
    - Health and readiness endpoints
    - API routers (users, etc.)
    """
    application = FastAPI(
        title=settings.service_name,
        version=settings.service_version,
        docs_url="/api/docs",  # Swagger UI at /api/docs
        redoc_url=None,  # Disable ReDoc
        openapi_url="/api/openapi.json",  # OpenAPI schema
    )

    # Enable CORS middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=_compute_cors_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.get("/health")
    def health() -> dict[str, str]:
        """Health check endpoint. Returns 'UP' if the service is alive."""
        return {"status": "UP"}

    @application.get("/ready")
    def ready() -> dict[str, str]:
        """Readiness check endpoint. Returns 'READY' if the service is ready to accept traffic."""
        return {"status": "READY"}

    # Register API routers
    application.include_router(users_router)

    return application


# Uvicorn entrypoint
# This is the symbol uvicorn will look for when starting the app
app: FastAPI = create_app()
