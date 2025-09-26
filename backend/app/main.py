from fastapi import FastAPI

from app.core.config import settings
from app.api.routes.opportunities import router as opp_router
from app.api.routes.odds import router as odds_router
from app.api.routes.golf import router as golf_router


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)

    app.include_router(opp_router)
    app.include_router(odds_router)
    app.include_router(golf_router)

    @app.get("/health")
    async def health() -> dict:
        return {"status": "ok"}

    @app.on_event("startup")
    async def on_startup() -> None:
        # Keep secrets out of logs; log non-sensitive config
        app.logger = getattr(app, "logger", None)
        if app.logger:
            app.logger.info(
                "App starting with refresh_interval_seconds=%s fee_cushion=%s",
                settings.refresh_interval_seconds,
                settings.fee_cushion,
            )

    return app


app = create_app()
