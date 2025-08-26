from __future__ import annotations

from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import settings


def _compute_cors_origins() -> list[str]:
    """
    Convertit settings.cors_origins (List[AnyHttpUrl] | List[str]) en list[str]
    et applique la règle: en dev si vide -> ["*"].
    """
    # settings.cors_origins peut contenir des AnyHttpUrl, on les cast en str.
    raw: List[str] = [str(o) for o in settings.cors_origins] if settings.cors_origins else []
    if settings.env.lower() == "dev" and not raw:
        return ["*"]
    return raw


def create_app() -> FastAPI:
    application = FastAPI(title=settings.service_name, version=settings.service_version)

    # CORS — mypy veut Sequence[str] | str → on fournit list[str]
    application.add_middleware(
        CORSMiddleware,
        allow_origins=_compute_cors_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.get("/health")
    def health() -> dict[str, str]:
        return {"status": "UP"}

    @application.get("/ready")
    def ready() -> dict[str, str]:
        return {"status": "READY"}

    return application


# Uvicorn importe ce symbole
app: FastAPI = create_app()
