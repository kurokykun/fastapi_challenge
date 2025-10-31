import strawberry
from uuid import UUID


@strawberry.type
class UserDTO:
    id: UUID
    email: str
    is_active: bool
