from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TagBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=255)

class TagCreate(TagBase):
    pass

class TagUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=255)

class TagInDB(TagBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Tag(TagInDB):
    pass
