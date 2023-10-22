import uuid
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, false, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import UUID
from app.database.base import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )

    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    fullname: Mapped[str] = mapped_column(String(50), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    is_activated: Mapped[bool] = mapped_column(server_default=false(), nullable=False)
    is_admin: Mapped[bool] = mapped_column(server_default=false(), nullable=False)

    @classmethod
    async def find(cls, db_session: AsyncSession, id: int):
        """
        :param db_session:
        :param name:
        :return:
        """
        stmt = select(cls).where(cls.id == id)
        result = await db_session.execute(stmt)
        instance: User | None = result.scalar_one_or_none()
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
        instance: User | None = result.scalar_one_or_none()
        return instance

    @classmethod
    async def find_by_email(cls, db_session: AsyncSession, email: str):
        """
        :param db_session:
        :param name:
        :return:
        """
        stmt = select(cls).where(cls.email == email)
        result = await db_session.execute(stmt)
        instance: User | None = result.scalar_one_or_none()
        return instance
