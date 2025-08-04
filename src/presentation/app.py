import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from presentation.exception_handlers import register_exception_handlers
from presentation.middleware.middleware import (
    ErrorContextMiddleware,
    LoggingMiddleware,
    RequestIDMiddleware,
    SecurityHeadersMiddleware,
)
from presentation.routes.router import app_router

# Configurar logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def create_app() -> FastAPI:
    """
    Factory para criar a aplicação FastAPI seguindo Clean Architecture.
    """
    app = FastAPI(
        title="Inner API",
        description="API seguindo princípios da Clean Architecture",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Middlewares - ordem importa! Os primeiros são executados por último na resposta
    # 1. Error Context - deve ser o primeiro para capturar exceções dos outros
    app.add_middleware(ErrorContextMiddleware)

    # 2. Security Headers
    app.add_middleware(SecurityHeadersMiddleware)

    # 3. Request ID
    app.add_middleware(RequestIDMiddleware)

    # 4. Logging
    app.add_middleware(LoggingMiddleware)

    # 5. CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Em produção, especificar origens permitidas
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Registrar exception handlers
    register_exception_handlers(app)

    # Registrar as rotas
    app.include_router(app_router)

    return app


# Instância da aplicação
app = create_app()
