from fastapi.routing import APIRouter

from fastapi_challenge.web.api import docs, monitoring, users

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(users.router)
api_router.include_router(docs.router)
