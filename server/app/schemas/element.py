from typing import Optional

from pydantic import BaseModel, ConfigDict


class CategoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str
    description: Optional[str] = None


class ElementRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str
    description: Optional[str] = None
    location: Optional[str] = None
    era: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[CategoryRead] = None
