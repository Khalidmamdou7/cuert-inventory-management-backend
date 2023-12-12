# registration of all system routes (fastapi)

from fastapi import APIRouter
from .auth.router import router as auth_router
from .teams.router import router as teams_router

routes = APIRouter()

routes.include_router(auth_router, prefix="/auth", tags=["auth"])
routes.include_router(teams_router, prefix="/teams", tags=["teams"])
