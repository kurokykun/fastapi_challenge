from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CommentBase(BaseModel):
    content: str
    post_id: UUID
    author_id: Optional[UUID] = None


class CommentCreate(CommentBase):
    pass


class CommentUpdate(BaseModel):
    content: Optional[str] = None


class CommentRead(CommentBase):
    id: UUID
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
