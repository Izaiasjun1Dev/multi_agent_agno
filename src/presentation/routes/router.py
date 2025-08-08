from fastapi import APIRouter

from presentation.routes.v1.route import api_v1_router

# Router principal da aplicação
app_router = APIRouter(prefix="/api")

# Registrar as rotas da API v1
app_router.include_router(api_v1_router)
