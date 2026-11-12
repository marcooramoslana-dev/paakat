import logging
from typing import Dict, Optional

from PIL import Image
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.repositories import element_repository, recognition_repository
from app.models.element import Element
from app.services.clip_service import clip_service

logger = logging.getLogger(__name__)

_DEFAULT_PROMPT = (
    "a photo of {name}, an ancient indigenous Mexican archaeological monument"
)


def _build_prompt(element: Element) -> str:
    if element.clip_prompt:
        return element.clip_prompt
    return _DEFAULT_PROMPT.format(name=element.name)


def recognize_image(
    db: Session,
    image: Image.Image,
    device_id: Optional[str] = None,
    image_path: Optional[str] = None,
) -> Dict:
    """Ejecuta CLIP zero-shot contra los elementos de la base de datos."""
    settings = get_settings()

    elements = element_repository.list_elements(db)
    if not elements:
        raise RuntimeError(
            "No hay elementos cargados en la base de datos. Ejecuta database/seed.sql"
        )

    labels = [element.name for element in elements]
    prompts = [_build_prompt(element) for element in elements]

    ranked = clip_service.classify(
        image, labels, prompts, top_k=max(settings.top_k, 1)
    )

    best_label, best_confidence = ranked[0]
    element = next(
        (candidate for candidate in elements if candidate.name == best_label), None
    )
    recognized = best_confidence >= settings.min_confidence and element is not None

    recognition = recognition_repository.create_recognition(
        db,
        label=best_label,
        confidence=best_confidence,
        image_path=image_path,
        device_id=device_id,
        element_id=element.id if element else None,
    )

    return {
        "recognized": recognized,
        "label": best_label,
        "confidence": best_confidence,
        "top_k": [
            {"label": label, "confidence": confidence}
            for label, confidence in ranked
        ],
        "element": element,
        "recognition_id": recognition.id,
    }
