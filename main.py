from app.models.base import Base
from config import initial_config as config
from app import create_app, fast_api_logger
from app.database import engine

app = create_app(config)


@app.on_event("shutdown")
async def shutdown_event():
    fast_api_logger.info("Shutting down...")


@app.on_event("startup")
async def startup_event():
    fast_api_logger.info("Starting up...")


@app.get("/")
async def home():
    return "backend service started"
