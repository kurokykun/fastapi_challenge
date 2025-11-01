from uuid import UUID

import strawberry
from strawberry.types import Info

from fastapi_challenge.db.dao.user_dao import UserDAO
from fastapi_challenge.db.models.users import get_jwt_strategy
from fastapi_challenge.web.gql.context import Context
from fastapi_challenge.web.gql.permissions import IsAuthenticated
from fastapi_challenge.web.gql.users.schema import AuthPayload, UserDTO


@strawberry.type
class Mutation:
    @strawberry.mutation(description="Update a user", permission_classes=[IsAuthenticated])
    async def update_user(
        self,
        info: Info[Context, None],
        id: UUID,
        email: str | None = None,
        is_active: bool | None = None,
    ) -> UserDTO | None:
        dao = UserDAO(info.context.db_connection)
        return await dao.update_user(id=id, email=email, is_active=is_active)

    @strawberry.mutation(description="Soft-delete a user", permission_classes=[IsAuthenticated])
    async def delete_user(self, info: Info[Context, None], id: UUID) -> bool:
        dao = UserDAO(info.context.db_connection)
        return await dao.delete_user(id=id)

    @strawberry.mutation(description="Register a new user")
    async def register_user(
        self,
        info: Info[Context, None],
        email: str,
        password: str,
        is_active: bool = True,
    ) -> UserDTO:
        dao = UserDAO(info.context.db_connection)
        user = await dao.create_user(email=email, password=password, is_active=is_active)
        return UserDTO(id=user.id, email=user.email, is_active=user.is_active)

    @strawberry.mutation(description="Authenticate a user and return a JWT")
    async def login_user(
        self,
        info: Info[Context, None],
        email: str,
        password: str,
    ) -> AuthPayload:
        dao = UserDAO(info.context.db_connection)
        user = await dao.authenticate_user(email=email, password=password)
        if not user:
            raise ValueError("Invalid credentials")
        strategy = get_jwt_strategy()
        access_token = await strategy.write_token(user)
        return AuthPayload(access_token=access_token, token_type="bearer")
