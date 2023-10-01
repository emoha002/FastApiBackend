from datetime import timedelta
from fastapi import APIRouter, Body, Request, Depends, BackgroundTasks, Response, status
from jose import jwt
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
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


users_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "IncorrectNot found"}},
)


oauth2_schema = OAuth2PasswordBearer(tokenUrl="./api_v1/auth/login")


@users_router.post("/login")
async def login(
    login_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db_session: AsyncSession = Depends(get_db),
):
    user: User | bool = await crud.authenticate_user(db_session, login_data)
    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_pydentic = user_schema.model_validate(user)

    access_token_expire_date = timedelta(crud.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = crud.create_access_token(
        data=user_pydentic.model_dump(), expires_delta=access_token_expire_date
    )
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: Annotated[str, Depends(oauth2_schema)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, crud.SECRET_KEY)
        if crud.has_time_passed(payload["exp"]):
            raise credentials_exception

        return payload

    except Exception:
        return credentials_exception


@users_router.get("/user/me", response_model=user_schema)
async def list2(user: Annotated[User, Depends(get_current_user)]):
    return user


@users_router.get("/")
async def read_items(request: Request, db_session: AsyncSession = Depends(get_db)):
    print(request)
    user = User(email="abel@a2sv.org", hashed_password="123")

    await user.save(db_session)
    # name: str = "".join(random.sample(string.ascii_lowercase, 4))

    # print("send the response")
    # logger = request.state.logger
    # logger.debug(f"save user {name}")
    return [{"username": "name"}, {"username": "name"}]


@users_router.post(
    "/add_user",
    response_model=user_schema,
)
async def create_user(
    user: Annotated[UserCreate, Body()], db_session: AsyncSession = Depends(get_db)
):
    db_user = await crud.get_user_by_username(db_session, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="username has already been taken")

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
