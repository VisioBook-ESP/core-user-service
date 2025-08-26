from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response
from prometheus_client import CollectorRegistry, CONTENT_TYPE_LATEST, generate_latest, Counter

from app.core.settings import settings

registry = CollectorRegistry()
HTTP_REQUESTS = Counter("http_requests_total", "Total HTTP requests", ["method","path","status"], registry=registry)

def create_app() -> FastAPI:
    app = FastAPI(title=settings.service_name, version=settings.service_version)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health(): return {"status": "UP"}

    @app.get("/ready")
    def ready(): return {"status": "READY"}

    @app.get("/metrics")
    def metrics(): return Response(generate_latest(registry), media_type=CONTENT_TYPE_LATEST)

    return app

app = create_app()
