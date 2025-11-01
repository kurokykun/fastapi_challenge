from typing import Optional

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.fastapi import BaseContext

from fastapi_challenge.db.dependencies import get_db_session
from fastapi_challenge.db.models.users import User, api_users


class Context(BaseContext):
    """Global graphql context."""

    def __init__(
        self,
        request: Request,
        db_connection: AsyncSession = Depends(get_db_session),
        user: Optional[User] = Depends(api_users.current_user(optional=True)),
    ) -> None:
        self.request: Request = request
        self.db_connection = db_connection
        self.user: Optional[User] = user
        self.request.state.user = user


def get_context(context: Context = Depends(Context)) -> Context:
    """
    Get custom context.

    :param context: graphql context.
    :return: context
    """
    return context
