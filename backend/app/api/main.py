from fastapi import APIRouter

from app.api.routes import login, private, users, utils, companies, technologies
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(private.router, prefix="/private", tags=["private"])
api_router.include_router(companies.router, prefix="/companies", tags=["companies"])
api_router.include_router(technologies.router, prefix="/technologies", tags=["technologies"])

if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
