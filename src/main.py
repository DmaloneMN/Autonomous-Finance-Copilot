"""FastAPI application entry point."""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from src.api.v1.router import api_router
from src.config import settings
from src.core.exceptions import AgentError, agent_error_handler, generic_error_handler
from src.core.logging import configure_logging
from src.core.middleware import RequestLoggingMiddleware, RequestTracingMiddleware

log = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    del app
    configure_logging(settings.log_level)
    log.info("startup", env=settings.app_env, version=settings.app_version)
    yield
    log.info("shutdown")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Autonomous Finance Copilot",
        description="Multi-agent AI platform for autonomous financial analysis",
        version=settings.app_version,
        lifespan=lifespan,
        docs_url="/docs" if settings.app_env != "production" else None,
        redoc_url="/redoc" if settings.app_env != "production" else None,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(RequestTracingMiddleware)

    app.include_router(api_router, prefix="/api/v1")
    app.add_exception_handler(AgentError, agent_error_handler)
    app.add_exception_handler(Exception, generic_error_handler)

    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)

    @app.get("/health", tags=["ops"])
    async def health() -> dict[str, str]:
        return {
            "status": "ok",
            "version": settings.app_version,
            "env": settings.app_env,
        }

    return app


app = create_app()
