import uuid
from datetime import datetime

from sqlalchemy import String, Enum, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm.properties import ForeignKey
from app.routers.api_v1.auth.models import User
from app.routers.api_v1.tasks.exceptions import TASK_NOT_FOUND

from app.routers.api_v1.tasks.schemas import (
    GetTasksFilterSchema,
    OrderBy,
    TaskState,
    TaskPriority,
    TaskColor,
)
from app.database.base import Base


class DBTask(Base):
    __tablename__ = "task"

    task_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        unique=True,
        index=True,
        primary_key=True,
    )

    user_id: Mapped["User"] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False
    )

    title: Mapped[str] = mapped_column(String(100), nullable=False)

    description: Mapped[str] = mapped_column(
        String(1000),
        nullable=True,
    )
    state: Mapped[TaskState] = mapped_column(
        Enum(TaskState),
        nullable=False,
    )
    priority: Mapped[TaskPriority] = mapped_column(
        Enum(TaskPriority),
        nullable=False,
    )
    color: Mapped[TaskColor] = mapped_column(
        Enum(TaskColor),
        nullable=False,
    )

    task_deadline: Mapped[datetime] = mapped_column(nullable=False)

    @classmethod
    async def get_task_by_id(
        cls, db_session: AsyncSession, task_id: uuid.UUID, user: User
    ):
        query = select(cls).where(cls.task_id == task_id, cls.user_id == user.id)
        print(query)
        result = await db_session.execute(query)

        instance: DBTask | None = result.scalars().one_or_none()

        if not instance:
            raise TASK_NOT_FOUND

        return instance

    @classmethod
    async def get_all_my_tasks(
        cls, db_session: AsyncSession, user: User, filter: GetTasksFilterSchema
    ):
        query = select(cls).where(cls.user_id == user.id)
        if filter.title:
            query = query.where(cls.title.ilike(f"%{filter.title}%"))
        if filter.state:
            query = query.where(cls.state == filter.state)
        if filter.priority:
            query = query.where(cls.priority == filter.priority)
        if filter.color:
            query = query.where(cls.color == filter.color)
        if filter.start_time:
            query = query.where(cls.task_deadline >= filter.start_time)
        if filter.end_time:
            query = query.where(cls.task_deadline <= filter.end_time)

        query = (
            query.order_by(cls.task_deadline.asc())
            if filter.order_by == OrderBy.ASC
            else query.order_by(cls.task_deadline.desc())
        )

        result = await db_session.execute(query)

        instance: list[DBTask] = list(result.scalars().all())

        return instance
