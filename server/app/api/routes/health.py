from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.config import get_settings
from app.services.clip_service import clip_service

router = APIRouter(tags=["health"])


@router.get("/health")
def health(db: Session = Depends(get_db)) -> dict:
    database_ok = True
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        database_ok = False

    settings = get_settings()
    return {
        "status": "ok" if database_ok else "degraded",
        "version": settings.app_version,
        "database": database_ok,
        "model_loaded": clip_service.loaded,
        "model_name": settings.clip_model_name,
    }
