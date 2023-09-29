from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schema import *
from app.models import User
from sqlalchemy import select


async def get_user(db_session: AsyncSession, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    result = await db_session.execute(stmt)
    user: User | None = result.scalars().first()
    return user


async def get_user_by_email(db_session: AsyncSession, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await db_session.execute(stmt)
    user: User | None = result.scalars().first()
    return user
    # return db.query(User).filter(User.email == email).first()


def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    pass
    # return db.query(User).offset(skip).limit(limit).all()


async def create_user(db_session: AsyncSession, user: UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(email=user.email, hashed_password=fake_hashed_password)
    await db_user.save(db_session)
    return db_user
