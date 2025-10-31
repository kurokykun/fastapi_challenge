"""Pydantic schemas for the application.

Keep schemas separated from ORM models to maintain separation of
responsibilities: these classes are used for request/response validation and
serialization.
"""

from .comment import CommentCreate, CommentRead, CommentUpdate
from .post import PostCreate, PostRead, PostUpdate

__all__ = [
    "PostCreate",
    "PostRead",
    "PostUpdate",
    "CommentCreate",
    "CommentRead",
    "CommentUpdate",
]
