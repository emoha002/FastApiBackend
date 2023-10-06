from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schema import *
from app.models import User
from sqlalchemy import select
from datetime import timedelta, datetime
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
import time


ALGORITHM = "HS256"
SECRET_KEY = "7724a39ad83427013e324274bd0edcc02283537ed581a4131efc3d6ec5137d57"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_user(db_session: AsyncSession, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    result = await db_session.execute(stmt)
    user: User | None = result.scalars().first()
    return user


async def authenticate_user(
    db_session, login_data: OAuth2PasswordRequestForm
) -> User | bool:
    user = await User.find_by_username(db_session, login_data.username)
    if not user:
        return False
    if not verify_password(login_data.password, user.hashed_password):
        return False
    return user


async def get_user_by_username(db_session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    result = await db_session.execute(stmt)
    user: User | None = result.scalars().first()
    return user
    # return db.query(User).filter(User.email == email).first()


def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    pass
    # return db.query(User).offset(skip).limit(limit).all()


async def create_user(db_session: AsyncSession, user: UserCreate):
    hashed_password = hash_password(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        fullname=user.fullname,
        hashed_password=hashed_password,
    )
    await db_user.save(db_session)
    return db_user
