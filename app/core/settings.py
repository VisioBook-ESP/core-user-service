from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from typing import List

class Settings(BaseSettings):
    service_name: str = "core-user-service"
    service_version: str = "1.0.0"
    env: str = "dev"
    port: int = 8080
    log_level: str = "info"
    cors_origins: List[AnyHttpUrl] | List[str] = []

    model_config = {"env_file": ".env", "case_sensitive": False}

settings = Settings()
