"""Echo API."""

from fastapi_challenge.web.gql.echo.mutation import Mutation
from fastapi_challenge.web.gql.echo.query import Query

__all__ = ["Query", "Mutation"]
