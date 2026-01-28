from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
from app.schemas.user import User


class CommentBase(BaseModel):
    content: str = Field(..., min_length=1)


class CommentCreate(CommentBase):
    post_id: int


class CommentUpdate(BaseModel):
    content: str = Field(..., min_length=1)


class CommentInDB(CommentBase):
    id: int
    author_id: int
    post_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class Comment(CommentInDB):
    author: User
