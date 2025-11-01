from __future__ import annotations

from strawberry.permission import BasePermission
from strawberry.types import Info


class IsAuthenticated(BasePermission):
    message = "Authentication required"

    def has_permission(self, source: object, info: Info, **kwargs) -> bool:
        user = getattr(info.context, "user", None)
        return bool(user and getattr(user, "is_active", False))
