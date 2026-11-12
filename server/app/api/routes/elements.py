from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.element import ElementRead
from app.services import element_service

router = APIRouter(prefix="/elements", tags=["elements"])


@router.get("", response_model=List[ElementRead])
def list_elements(db: Session = Depends(get_db)):
    return element_service.list_elements(db)


@router.get("/{slug}", response_model=ElementRead)
def get_element(slug: str, db: Session = Depends(get_db)):
    element = element_service.get_element_by_slug(db, slug)
    if element is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Elemento no encontrado",
        )
    return element
