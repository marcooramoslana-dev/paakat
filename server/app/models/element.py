from typing import List, Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Element(Base):
    __tablename__ = "elements"

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"), default=None
    )
    name: Mapped[str] = mapped_column(String(160), unique=True, index=True)
    slug: Mapped[str] = mapped_column(String(160), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, default=None)
    location: Mapped[Optional[str]] = mapped_column(String(255), default=None)
    era: Mapped[Optional[str]] = mapped_column(String(120), default=None)
    image_url: Mapped[Optional[str]] = mapped_column(String(500), default=None)
    # Texto en ingles optimizado para el prompt de CLIP (si es null se autogenera)
    clip_prompt: Mapped[Optional[str]] = mapped_column(Text, default=None)

    category: Mapped[Optional["Category"]] = relationship(back_populates="elements")
    recognitions: Mapped[List["Recognition"]] = relationship(back_populates="element")
