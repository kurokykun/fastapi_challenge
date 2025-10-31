from typing import List

import strawberry
from strawberry.types import Info

from fastapi_challenge.db.dao.comment_dao import CommentDAO
from fastapi_challenge.web.gql.context import Context
from fastapi_challenge.web.gql.comments.schema import CommentDTO


@strawberry.type
class Query:
    @strawberry.field(description="Get all comments")
    async def get_comments(
        self,
        info: Info[Context, None],
        limit: int = 15,
        offset: int = 0,
    ) -> List[CommentDTO]:
        dao = CommentDAO(info.context.db_connection)
        return await dao.get_all_comments(limit=limit, offset=offset)  # type: ignore
