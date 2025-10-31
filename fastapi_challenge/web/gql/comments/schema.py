import strawberry
from uuid import UUID
from typing import Optional


@strawberry.type
class CommentDTO:
    id: UUID
    content: str
    post_id: UUID
    author_id: Optional[UUID]
