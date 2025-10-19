from __future__ import annotations

from fastapi import FastAPI

from best_occasion.api.routes import recommendations, registry


def create_app() -> FastAPI:
    """Create and configure a FastAPI application instance."""

    app = FastAPI(title="best-occasion", version="0.1.0")
    app.include_router(recommendations.router)
    app.include_router(registry.router)
    return app
