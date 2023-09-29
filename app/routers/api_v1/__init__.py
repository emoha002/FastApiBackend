from fastapi import APIRouter
from .users import users_router
api_v1_router = APIRouter(prefix='/api_v1')

api_v1_router.include_router(users_router)
