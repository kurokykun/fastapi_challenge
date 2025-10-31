from typing import List

import strawberry
from strawberry.types import Info

from fastapi_challenge.db.dao.post_dao import PostDAO
from fastapi_challenge.web.gql.context import Context
from fastapi_challenge.web.gql.posts.schema import PostDTO


@strawberry.type
class Query:
    @strawberry.field()
    async def get_posts(
        self,
        info: Info[Context, None],
        limit: int = 15,
        offset: int = 0,
    ) -> List[PostDTO]:
        dao = PostDAO(info.context.db_connection)
        return await dao.get_all_posts(limit=limit, offset=offset)
