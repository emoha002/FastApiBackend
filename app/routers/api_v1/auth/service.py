from datetime import timedelta, datetime
import time


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.routers.api_v1.auth.exceptions import (
    ALREADY_REGISTERED,
    INCORRECT_PASSWORD,
    USER_NAME_IS_TAKEN,
    USER_NOT_FOUND,
)

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

from app.routers.api_v1.auth.models import User

from .constants import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from .schemas import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def has_time_passed(time_to_check):
    current_time = time.time()
    return current_time > time_to_check


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    to_encode.update({"id": str(to_encode.get("id"))})
    # pop created_at operation

    to_encode.pop("created_at")

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_user(db_session: AsyncSession, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    result = await db_session.execute(stmt)
    user: User | None = result.scalars().first()
    return user


async def authenticate_user(db_session, login_data: OAuth2PasswordRequestForm) -> User:
    user = await User.find_by_username(db_session, login_data.username)
    if not user:
        raise USER_NOT_FOUND
    if not verify_password(login_data.password, user.hashed_password):
        raise INCORRECT_PASSWORD
    return user


async def get_user_by_username(db_session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    result = await db_session.execute(stmt)
    user: User | None = result.scalar_one_or_none()
    return user


# def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
#     return db.query(User).offset(skip).limit(limit).all()


async def create_user(db_session: AsyncSession, user: UserCreate):
    # check if user exists by this email address
    db_user = await get_user_by_username(db_session, username=user.username)
    if db_user:
        raise USER_NAME_IS_TAKEN

    existing_user = await User.find_by_email(db_session, user.email)

    if existing_user:
        raise ALREADY_REGISTERED

    hashed_password = hash_password(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        fullname=user.fullname,
        hashed_password=hashed_password,
    )
    await db_user.save(db_session)
    return db_user
