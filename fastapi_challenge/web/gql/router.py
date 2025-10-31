import strawberry
from strawberry.fastapi import GraphQLRouter

from fastapi_challenge.web.gql import dummy, echo
from fastapi_challenge.web.gql.context import Context, get_context


@strawberry.type
class Query(
    echo.Query,
    dummy.Query,
):
    """Main query."""


@strawberry.type
class Mutation(
    echo.Mutation,
    dummy.Mutation,
):
    """Main mutation."""


schema = strawberry.Schema(
    Query,
    Mutation,
)

gql_router: GraphQLRouter[Context, None] = GraphQLRouter(
    schema,
    graphiql=True,
    context_getter=get_context,
)
