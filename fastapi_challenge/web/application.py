import logging
from importlib import metadata
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from fastapi.staticfiles import StaticFiles

from fastapi_challenge.web.api.router import api_router
from fastapi_challenge.web.lifespan import lifespan_setup
from fastapi_challenge.web.middleware import setup_middlewares

APP_ROOT = Path(__file__).parent.parent


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="fastapi_challenge",
        version=metadata.version("fastapi_challenge"),
        lifespan=lifespan_setup,
        docs_url=None,
        redoc_url=None,
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )
    
    setup_middlewares(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")
    # Graphql router: imported lazily to avoid optional dependency import errors
    try:
        # local import to prevent import-time failures when strawberry/pydantic
        # compatibility issues occur in the environment. If GraphQL support is
        # required, ensure compatible versions of dependencies are installed.
        from fastapi_challenge.web.gql.router import gql_router

        app.include_router(router=gql_router, prefix="/graphql")
    except Exception as exc:  # pragma: no cover - defensive: environment may vary
        # Log the error and continue without GraphQL routes so the app can start.
        logging.getLogger(__name__).warning(
            "GraphQL router could not be mounted due to import error: %s",
            exc,
        )
    # Adds static directory.
    # This directory is used to access swagger files.
    app.mount("/static", StaticFiles(directory=APP_ROOT / "static"), name="static")

    return app
