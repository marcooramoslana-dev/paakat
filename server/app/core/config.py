from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = "Paakat Recognition API"
    app_version: str = "1.0.0"
    debug: bool = False

    api_prefix: str = "/api/v1"
    api_key: str = ""  # si se deja vacio, la proteccion por API key queda desactivada

    # Base de datos
    database_url: str = (
        "mysql+pymysql://paakat:paakat@localhost:3306/paakat?charset=utf8mb4"
    )

    # Modelo de vision (CLIP zero-shot)
    clip_model_name: str = "openai/clip-vit-base-patch32"
    clip_device: str = "auto"  # auto | cpu | cuda
    min_confidence: float = 0.30
    top_k: int = 3

    # Imagenes
    upload_dir: str = "uploads"
    max_upload_mb: int = 10

    # CORS
    cors_origins: List[str] = ["*"]


@lru_cache()
def get_settings() -> Settings:
    return Settings()
