from fastapi import FastAPI
import json
from starlette.responses import JSONResponse

from app.core.config import settings
from app.api.routes.opportunities import router as opp_router
from app.api.routes.odds import router as odds_router
from app.api.routes.golf import router as golf_router
from app.api.routes.debug import router as debug_router


class PrettyJSONResponse(JSONResponse):
    def render(self, content) -> bytes:  # type: ignore[override]
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=2,
            separators=(", ", ": "),
        ).encode("utf-8")


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, default_response_class=PrettyJSONResponse)

    app.include_router(opp_router)
    app.include_router(odds_router)
    app.include_router(golf_router)
    app.include_router(debug_router)

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
