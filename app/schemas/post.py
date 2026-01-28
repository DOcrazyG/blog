from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List
from app.schemas.user import User
from app.schemas.tag import Tag


class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str
    summary: Optional[str] = Field(None, max_length=500)
    is_published: bool = False
    tag_ids: Optional[List[int]] = []


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = None
    summary: Optional[str] = Field(None, max_length=500)
    is_published: Optional[bool] = None
    tag_ids: Optional[List[int]] = []


class PostInDB(PostBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    published_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class Post(PostInDB):
    author: User
    tags: List[Tag]
