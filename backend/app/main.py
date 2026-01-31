from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.db_ping import router as db_router
from app.api.health import router as health_router
from app.api.import_csv import router as import_router
from app.api.transactions import router as transactions_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.api.analytics import router as analytics_router



def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
    )

    origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(db_router)

    app.include_router(transactions_router)

    app.include_router(health_router)

    app.include_router(import_router)

    app.include_router(analytics_router)


    return app


app = create_app()
