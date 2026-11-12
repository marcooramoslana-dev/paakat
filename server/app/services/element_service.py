from typing import List

from sqlalchemy.orm import Session

from app.db.repositories import element_repository
from app.models.element import Element


def list_elements(db: Session) -> List[Element]:
    return element_repository.list_elements(db)


def get_element_by_slug(db: Session, slug: str):
    return element_repository.get_element_by_slug(db, slug)
