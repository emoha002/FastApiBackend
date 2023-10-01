from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, select, Integer
from app.models.base import Base
from sqlalchemy.ext.asyncio import AsyncSession


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(200), nullable=False)

    @classmethod
    async def find(cls, db_session: AsyncSession, id: int):
        """
        :param db_session:
        :param name:
        :return:
        """
        stmt = select(cls).where(cls.id == id)
        result = await db_session.execute(stmt)
        instance: User | None = result.scalars().first()
        return instance

    @classmethod
    async def find_by_username(cls, db_session: AsyncSession, username: str):
        """
        :param db_session:
        :param name:
        :return:
        """
        stmt = select(cls).where(cls.username == username)
        result = await db_session.execute(stmt)
        instance: User | None = result.scalars().first()
        return instance
