from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.element import ElementRead


class Candidate(BaseModel):
    label: str
    confidence: float


class RecognitionResponse(BaseModel):
    recognized: bool
    label: str
    confidence: float
    top_k: List[Candidate]
    element: Optional[ElementRead] = None
    recognition_id: Optional[int] = None


class RecognitionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    label: str
    confidence: float
    image_path: Optional[str] = None
    device_id: Optional[str] = None
    element_id: Optional[int] = None
    created_at: Optional[datetime] = None
