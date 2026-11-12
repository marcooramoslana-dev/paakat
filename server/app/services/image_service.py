import os
import uuid
from pathlib import Path

from app.core.config import get_settings

_ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp"}


def save_image(data: bytes, filename: str) -> str:
    """Guarda la imagen en disco y devuelve la ruta relativa."""
    settings = get_settings()
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)

    ext = os.path.splitext(filename or "")[1].lower()
    if ext not in _ALLOWED_EXT:
        ext = ".jpg"

    name = f"{uuid.uuid4().hex}{ext}"
    path = upload_dir / name
    with open(path, "wb") as handle:
        handle.write(data)

    return path.as_posix()
