from fastapi import APIRouter, Body, Request, Depends, BackgroundTasks
from pytest import importorskip
from sqlalchemy.ext.asyncio import AsyncSession
import random
import string
from app.database import get_db
from app.models.user import User
import asyncio
from fastapi import HTTPException
from app.controler import crud
from app.schemas.user_schema import User as user_schema, UserCreate
from typing import Annotated

users_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "IncorrectNot found"}},
)


@users_router.get("/")
async def read_items(request: Request, db_session: AsyncSession = Depends(get_db)):
    print(request)
    print("got here")

    user = User(email="abel@a2sv.org", hashed_password="123")

    await user.save(db_session)
    # name: str = "".join(random.sample(string.ascii_lowercase, 4))

    # print("send the response")
    # logger = request.state.logger
    # logger.debug(f"save user {name}")
    return [{"username": "name"}, {"username": "name"}]


@users_router.post("/add_user", response_model=user_schema)
async def create_user(user: Annotated[UserCreate, Body()], db_session: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_email(db_session, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return await crud.create_user(db_session=db_session, user=user)


# @app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


@users_router.get("/users/{user_id}", response_model=user_schema)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user(db, user_id=user_id)
    print(db_user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
