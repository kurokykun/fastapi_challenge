import strawberry
from uuid import UUID


@strawberry.type
class PostDTO:
    id: UUID
    title: str
    content: str
    author_id: UUID
