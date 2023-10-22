from typing import Annotated
from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db
from app.routers.api_v1.auth.models import User
from app.routers.api_v1.auth.schemas import UserCreate, UserSchema
from app.routers.api_v1.auth.service import (
    authenticate_user,
    create_access_token,
    create_user,
)
from app.routers.api_v1.auth.dependencies import get_current_user

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Incorrect Not found"}},
)


GOOGLE_CLIENT_SECRET: str = "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"


@auth_router.get("/")
async def root():
    return {"message": "Hello World"}


@auth_router.post(
    "/sign_up",
    response_model=UserSchema,
)
async def create_new_user(
    user: Annotated[UserCreate, Body()], db_session: AsyncSession = Depends(get_db)
):
    return await create_user(db_session=db_session, user=user)


@auth_router.post("/sign_in")
async def sign_in(
    login_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db_session: AsyncSession = Depends(get_db),
):
    user: User = await authenticate_user(db_session, login_data)

    user_pydentic = UserSchema.model_validate(user)

    access_token = create_access_token(data=user_pydentic.model_dump())
    return {"access_token": access_token, "token_type": "bearer", "user": user_pydentic}


@auth_router.get("/user/me", response_model=UserSchema)
async def my_account(user: Annotated[User, Depends(get_current_user)]):
    return user


# @auth_router.get("/users/{user_id}", response_model=user_schema)
# async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
#     db_user = await crud.get_user(db, user_id=user_id)
#     print(db_user)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user
