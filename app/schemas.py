from pydantic import BaseModel, Field
from datetime import datetime


class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)


class Item(BaseModel):
    id: int
    name: str
    created_at: datetime