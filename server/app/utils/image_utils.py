import io
import logging

from fastapi import HTTPException, status
from PIL import Image, UnidentifiedImageError

logger = logging.getLogger(__name__)

MAX_SIDE = 1024


def load_image_bytes(data: bytes, max_mb: int) -> Image.Image:
    """Valida y decodifica la imagen subida por los lentes."""
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Archivo vacio",
        )

    if len(data) > max_mb * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"El archivo supera {max_mb} MB",
        )

    try:
        image = Image.open(io.BytesIO(data))
        image.load()
    except (UnidentifiedImageError, OSError) as exc:
        logger.warning("Imagen invalida: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de imagen invalido",
        )

    if image.mode != "RGB":
        image = image.convert("RGB")

    if max(image.size) > MAX_SIDE:
        image.thumbnail((MAX_SIDE, MAX_SIDE))

    return image
