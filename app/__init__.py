from fastapi import FastAPI, Request
from config import Config
from app.routers.api_v1 import api_v1_router
from app.utils.logger import fast_api_logger


async def logger_middleware(request: Request, call_next):
    request.state.logger = fast_api_logger
    response = await call_next(request)
    return response


def create_app(config: Config, lifespan) -> FastAPI:
    fast_api_logger.info(f"App started as {config.CONFIG_TYPE}")
    app = FastAPI(title="Scheduling Project", lifespan=lifespan)
    app.include_router(api_v1_router)
    app.middleware("http")(logger_middleware)

    return app
