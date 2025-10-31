from typing import Optional
from uuid import UUID

import strawberry
from strawberry.types import Info

from fastapi_challenge.db.dao.user_dao import UserDAO
from fastapi_challenge.web.gql.context import Context
from fastapi_challenge.web.gql.users.schema import UserDTO


@strawberry.type
class Mutation:
    """Mutations for users."""

    @strawberry.mutation(description="Update a user")
    async def update_user(
        self,
        info: Info[Context, None],
        id: UUID,
        email: str | None = None,
        is_active: bool | None = None,
    ) -> UserDTO | None:
        dao = UserDAO(info.context.db_connection)
        return await dao.update_user(id=id, email=email, is_active=is_active)

    @strawberry.mutation(description="Soft-delete a user")
    async def delete_user(self, info: Info[Context, None], id: UUID) -> bool:
        dao = UserDAO(info.context.db_connection)
        return await dao.delete_user(id=id)
