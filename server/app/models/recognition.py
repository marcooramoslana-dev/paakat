from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Recognition(Base):
    __tablename__ = "recognitions"

    id: Mapped[int] = mapped_column(primary_key=True)
    element_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("elements.id", ondelete="SET NULL"), default=None
    )
    label: Mapped[str] = mapped_column(String(160), index=True)
    confidence: Mapped[float] = mapped_column(Float)
    image_path: Mapped[Optional[str]] = mapped_column(String(500), default=None)
    device_id: Mapped[Optional[str]] = mapped_column(String(120), default=None)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    element: Mapped[Optional["Element"]] = relationship(back_populates="recognitions")
