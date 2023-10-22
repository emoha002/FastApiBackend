from fastapi import APIRouter
from app.routers.api_v1.auth.router import auth_router


api_v1_router = APIRouter(prefix="/api_v1")
api_v1_router.include_router(auth_router)
