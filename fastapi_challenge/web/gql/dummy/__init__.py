"""Package for dummy model."""

from fastapi_challenge.web.gql.dummy.mutation import Mutation
from fastapi_challenge.web.gql.dummy.query import Query

__all__ = ["Query", "Mutation"]
