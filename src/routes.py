# registration of all system routes (fastapi)

from fastapi import APIRouter
from .auth.router import router as auth_router
from .teams.router import router as teams_router
from .items.router import router as items_router
from .item_requests.router import router as item_requests_router
from .suppliers.router import router as suppliers_router

routes = APIRouter()

routes.include_router(auth_router, prefix="/auth", tags=["auth"])
routes.include_router(teams_router, prefix="/teams", tags=["teams"])
routes.include_router(items_router, prefix="/items", tags=["items"])
routes.include_router(item_requests_router, prefix="/item-requests", tags=["item-requests"])
routes.include_router(suppliers_router, prefix="/suppliers", tags=["suppliers"])