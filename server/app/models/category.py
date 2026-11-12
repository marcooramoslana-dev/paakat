from typing import List, Optional

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, default=None)

    elements: Mapped[List["Element"]] = relationship(back_populates="category")
