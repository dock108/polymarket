from fastapi import FastAPI

from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)

    @app.get("/health")
    async def health() -> dict:
        return {"status": "ok"}

    @app.on_event("startup")
    async def on_startup() -> None:
        # Keep secrets out of logs; log non-sensitive config
        app.logger = getattr(app, "logger", None)
        if app.logger:
            app.logger.info("App starting with refresh_interval_seconds=%s fee_cushion=%s", settings.refresh_interval_seconds, settings.fee_cushion)

    return app


app = create_app()
