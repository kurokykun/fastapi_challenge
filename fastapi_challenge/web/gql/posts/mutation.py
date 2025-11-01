from uuid import UUID

import strawberry
from strawberry.types import Info

from fastapi_challenge.db.dao.post_dao import PostDAO
from fastapi_challenge.web.gql.context import Context
from fastapi_challenge.web.gql.permissions import IsAuthenticated, IsPostOwner
from fastapi_challenge.web.gql.posts.schema import PostDTO


@strawberry.type
class Mutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def create_post(
        self,
        info: Info[Context, None],
        title: str,
        content: str,
        author_id: UUID,
    ) -> str:
        dao = PostDAO(info.context.db_connection)
        await dao.create_post(title=title, content=content, author_id=author_id)
        return title

    @strawberry.mutation(permission_classes=[IsAuthenticated, IsPostOwner])
    async def update_post(
        self,
        info: Info[Context, None],
        id: UUID,
        title: str | None = None,
        content: str | None = None,
    ) -> PostDTO | None:
        dao = PostDAO(info.context.db_connection)
        return await dao.update_post(id=id, title=title, content=content)

    @strawberry.mutation(permission_classes=[IsAuthenticated, IsPostOwner])
    async def delete_post(self, info: Info[Context, None], id: UUID) -> bool:
        dao = PostDAO(info.context.db_connection)
        return await dao.delete_post(id=id)
