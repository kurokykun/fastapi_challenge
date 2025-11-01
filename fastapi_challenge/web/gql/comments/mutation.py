from typing import Optional
from uuid import UUID

import strawberry
from strawberry.types import Info

from fastapi_challenge.db.dao.comment_dao import CommentDAO
from fastapi_challenge.web.gql.context import Context
from fastapi_challenge.web.gql.permissions import IsAuthenticated
from fastapi_challenge.web.gql.comments.schema import CommentDTO


@strawberry.type
class Mutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def create_comment(
        self,
        info: Info[Context, None],
        content: str,
        post_id: UUID,
        author_id: Optional[UUID] = None,
    ) -> str:
        dao = CommentDAO(info.context.db_connection)
        await dao.create_comment(content=content, post_id=post_id, author_id=author_id)
        return content

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def update_comment(
        self,
        info: Info[Context, None],
        id: UUID,
        content: str | None = None,
    ) -> CommentDTO | None:
        dao = CommentDAO(info.context.db_connection)
        return await dao.update_comment(id=id, content=content)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def delete_comment(self, info: Info[Context, None], id: UUID) -> bool:
        dao = CommentDAO(info.context.db_connection)
        return await dao.delete_comment(id=id)
