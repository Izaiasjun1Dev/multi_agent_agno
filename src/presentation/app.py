from fastapi import FastAPI

from presentation.routes.router import app_router


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

    # Registrar as rotas
    app.include_router(app_router)

    return app


# Instância da aplicação
app = create_app()
