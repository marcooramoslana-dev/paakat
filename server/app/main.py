import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.concurrency import run_in_threadpool

import app.models  # noqa: F401  (registra modelos en Base.metadata)
from app.api.routes import elements, health, recognition
from app.core.config import get_settings
from app.core.logging import setup_logging
from app.db.base import Base
from app.db.session import engine
from app.services.clip_service import clip_service

settings = get_settings()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    setup_logging("DEBUG" if settings.debug else "INFO")

    try:
        Base.metadata.create_all(bind=engine)
    except Exception as exc:  # noqa: BLE001
        logger.warning("No se pudieron crear las tablas al inicio: %s", exc)

    try:
        await run_in_threadpool(clip_service.load)
    except Exception as exc:  # noqa: BLE001
        logger.warning(
            "No se pudo precargar CLIP (se cargara en la primera peticion): %s",
            exc,
        )

    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

app.include_router(health.router)
app.include_router(elements.router, prefix=settings.api_prefix)
app.include_router(recognition.router, prefix=settings.api_prefix)


@app.get("/", tags=["root"])
def root() -> dict:
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "api_prefix": settings.api_prefix,
    }
