from fastapi import APIRouter

from presentation.routes.v1.user.user_routes import router as user_router
from presentation.routes.v1.auth.auth_routes import router as auth_router

# Router principal da API v1
api_v1_router = APIRouter(prefix="/v1")
api_v1_router.include_router(user_router)
api_v1_router.include_router(auth_router)
