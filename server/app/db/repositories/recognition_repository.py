from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.recognition import Recognition


def create_recognition(
    db: Session,
    *,
    label: str,
    confidence: float,
    image_path: Optional[str] = None,
    device_id: Optional[str] = None,
    element_id: Optional[int] = None,
) -> Recognition:
    recognition = Recognition(
        label=label,
        confidence=confidence,
        image_path=image_path,
        device_id=device_id,
        element_id=element_id,
    )
    db.add(recognition)
    db.commit()
    db.refresh(recognition)
    return recognition


def list_recognitions(db: Session, limit: int = 50) -> List[Recognition]:
    stmt = (
        select(Recognition)
        .options(selectinload(Recognition.element))
        .order_by(Recognition.created_at.desc(), Recognition.id.desc())
        .limit(limit)
    )
    return list(db.scalars(stmt).all())
