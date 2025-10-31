import strawberry
from strawberry.fastapi import GraphQLRouter

from fastapi_challenge.web.gql import dummy, echo,posts,users,comments
from fastapi_challenge.web.gql.context import Context, get_context


@strawberry.type
class Query(
    echo.Query,
    dummy.Query,
    posts.Query,
    users.Query,
    comments.Query
):
    """Main query."""


@strawberry.type
class Mutation(
    echo.Mutation,
    dummy.Mutation,
    posts.Mutation,
    users.Mutation,
    comments.Mutation,
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
