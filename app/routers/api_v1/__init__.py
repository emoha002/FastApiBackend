from fastapi import APIRouter
from app.routers.api_v1.auth.router import auth_router
from app.routers.api_v1.events.router import event_router

api_v1_router = APIRouter(prefix="/api_v1")
api_v1_router.include_router(auth_router)
api_v1_router.include_router(event_router)
