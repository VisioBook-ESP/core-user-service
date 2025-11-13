"""
Application entrypoint for Core User Service.
Initializes FastAPI app, CORS, health/ready endpoints, and API routers.
"""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.core.database import SessionLocal
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
        redoc_url="/api/redoc",  # ReDoc at /api/redoc
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
        """
        Health check endpoint with service metadata.

        Returns:
            status: "UP" if the service is alive
            timestamp: Current UTC timestamp (ISO 8601)
            service: Service name
            version: Service version
        """
        return {
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),  # noqa: UP017
            "service": settings.service_name,
            "version": settings.service_version,
        }

    @application.get("/ready")
    def ready() -> dict[str, str]:
        """Readiness check endpoint. Returns 'READY' if the service is ready to accept traffic."""
        return {"status": "READY"}

    @application.get("/health-db")
    def health_db() -> dict[str, str]:
        """
        Database health check endpoint.

        Executes a simple SQL query (SELECT 1) to verify database connectivity.

        Returns:
            200 OK with {"status": "healthy", "database": "connected"} if DB is accessible
            503 Service Unavailable if DB connection fails
        """
        try:
            db = SessionLocal()
            db.execute(text("SELECT 1"))
            db.close()
            return {"status": "healthy", "database": "connected"}
        except Exception as exc:
            # Raise 503 Service Unavailable if DB is down
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Database unavailable: {str(exc)}",
            ) from exc

    # Register API routers
    application.include_router(users_router)
    application.include_router(auth_router)

    return application


# Uvicorn entrypoint
# This is the symbol uvicorn will look for when starting the app
app: FastAPI = create_app()
