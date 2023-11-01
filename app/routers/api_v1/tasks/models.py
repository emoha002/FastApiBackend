import uuid
from datetime import datetime

from sqlalchemy import String, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.routers.api_v1.tasks.schemas import TaskState, TaskPriority
from app.database.base import Base


class Taks(Base):
    __tablename__ = "task"

    task_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        unique=True,
        index=True,
        primary_key=True,
    )

    description: Mapped[str] = mapped_column(
        String(1000),
        nullable=True,
    )
    state: Mapped[TaskState] = mapped_column(
        Enum(TaskState),
        nullable=False,
    )
    task_priority: Mapped[TaskPriority] = mapped_column(
        Enum(TaskPriority),
        nullable=False,
    )
    task_deadline: Mapped[datetime] = mapped_column(nullable=False)
    reminder_after: Mapped[datetime] = mapped_column(nullable=False)
