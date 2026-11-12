from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.element import Element


def list_elements(db: Session) -> List[Element]:
    stmt = (
        select(Element)
        .options(selectinload(Element.category))
        .order_by(Element.name)
    )
    return list(db.scalars(stmt).all())


def get_element_by_slug(db: Session, slug: str) -> Optional[Element]:
    stmt = (
        select(Element)
        .where(Element.slug == slug)
        .options(selectinload(Element.category))
    )
    return db.scalars(stmt).first()


def get_element(db: Session, element_id: int) -> Optional[Element]:
    stmt = (
        select(Element)
        .where(Element.id == element_id)
        .options(selectinload(Element.category))
    )
    return db.scalars(stmt).first()
