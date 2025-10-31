from typing import List

import strawberry
from strawberry.types import Info

from fastapi_challenge.db.dao.user_dao import UserDAO
from fastapi_challenge.web.gql.context import Context
from fastapi_challenge.web.gql.users.schema import UserDTO


@strawberry.type
class Query:
    @strawberry.field()
    async def get_users(
        self,
        info: Info[Context, None],
        limit: int = 15,
        offset: int = 0,
    ) -> List[UserDTO]:
        dao = UserDAO(info.context.db_connection)
        return await dao.get_all_users(limit=limit, offset=offset)
