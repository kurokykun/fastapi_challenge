from fastapi import FastAPI

from .process_time import ProcessTimeHeaderMiddleware


def setup_middlewares(app: FastAPI) -> None:
    app.add_middleware(ProcessTimeHeaderMiddleware)
