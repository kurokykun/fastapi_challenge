from __future__ import annotations

from strawberry.permission import BasePermission
from strawberry.types import Info
from fastapi_challenge.db.dao.post_dao import PostDAO


class IsAuthenticated(BasePermission):
    message = "Authentication required"
    def has_permission(self, source: object, info: Info, **kwargs) -> bool:
        user = getattr(info.context, "user", None)
        return bool(user and getattr(user, "is_active", False))


class IsPostOwner(BasePermission):
    message = "You can only modify your own posts"
    async def has_permission(self, source: object, info: Info, **kwargs) -> bool:
        user = getattr(info.context, "user", None)
        if not user or not getattr(user, "is_active", False):
            return False
        post_id = kwargs.get("id")
        if post_id is None:
            return False
        dao = PostDAO(info.context.db_connection)
        post = await dao.get_by_id(post_id)
        return bool(post and getattr(post, "author_id", None) == getattr(user, "id", None))
