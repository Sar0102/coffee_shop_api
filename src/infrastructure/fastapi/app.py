from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.ui.api.routers import auth, users
from src.ui.errors import install_error_handlers


def create_app() -> FastAPI:
    """Build FastAPI application."""
    app_ = FastAPI(title="Coffee Shop API - Users", version="1.0.0")

    app_.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=[],
    )

    install_error_handlers(app_)
    app_.include_router(auth.router)
    app_.include_router(users.router)

    return app_
