from contextlib import asynccontextmanager

from fastapi import FastAPI
from config import initial_config as config
from app import create_app, fast_api_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    fast_api_logger.info("Starting up ...")
    yield
    fast_api_logger.info("Shutting down ...")


app = create_app(config, lifespan=lifespan)


@app.get("/")
async def home():
    return {"message": "backend service started"}
