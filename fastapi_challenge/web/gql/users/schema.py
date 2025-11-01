from uuid import UUID

import strawberry  # type: ignore[import]


@strawberry.type
class UserDTO:
    id: UUID
    email: str
    is_active: bool


@strawberry.type
class AuthPayload:
    access_token: str
    token_type: str = strawberry.field(default="bearer")
