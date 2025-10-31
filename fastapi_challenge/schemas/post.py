from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class PostBase(BaseModel):
    title: str = Field(..., max_length=255)
    content: str
    author_id: UUID


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    content: Optional[str] = None


class PostRead(PostBase):
    id: UUID
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
