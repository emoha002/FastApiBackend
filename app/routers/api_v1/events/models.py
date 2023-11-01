from datetime import datetime
from sqlalchemy import and_
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm.properties import ForeignKey
from sqlalchemy import String, select
from app.database.base import Base
from app.routers.api_v1.auth.models import User
from app.routers.api_v1.events.exceptions import EventOccuranceNotFoundHTTPException


class CalendarEvent(Base):
    __tablename__ = "calendar_event"

    event_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        unique=True,
        index=True,
        primary_key=True,
    )
    user_id: Mapped["User"] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False
    )
    event_name: Mapped[str] = mapped_column(String(200), nullable=False)
    course_number: Mapped[str] = mapped_column(String(200), nullable=True)
    description: Mapped[str] = mapped_column(String(500), nullable=True)

    event_started_at: Mapped[datetime] = mapped_column(nullable=False)

    repeat_until: Mapped[datetime] = mapped_column(nullable=False)

    event_occurrences: Mapped[list["EventOccurrence"]] = relationship(
        "EventOccurrence",
        back_populates="event",
        cascade="all, delete",
        passive_deletes=True,
    )

    # async def get_all_events_by_range(
    #     user: User,
    #     date_range: DateRangeGetEvent,
    # ):
    #     return 10
    #     pass


class EventOccurrence(Base):
    __tablename__ = "event_occurrence"

    occurrence_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        unique=True,
        index=True,
        primary_key=True,
    )

    event_id: Mapped["CalendarEvent"] = mapped_column(
        UUID(as_uuid=True), ForeignKey("calendar_event.event_id"), nullable=False
    )

    start_time: Mapped[datetime] = mapped_column(nullable=False)
    end_time: Mapped[datetime] = mapped_column(nullable=False)

    location: Mapped[str] = mapped_column(String(200), nullable=True)
    description: Mapped[str] = mapped_column(String(500), nullable=True)

    event: Mapped[CalendarEvent] = relationship(
        "CalendarEvent", back_populates="event_occurrences"
    )

    @classmethod
    async def get_by_occurance_id(
        cls,
        db_session: AsyncSession,
        occurance_id: uuid.UUID,
        user: User,
    ):
        query = (
            select(cls)
            .join(CalendarEvent, CalendarEvent.event_id == cls.event_id)
            .where(
                and_(
                    cls.occurrence_id == occurance_id,
                    CalendarEvent.user_id == user.id,
                )
            )
            .options(selectinload(cls.event))
        )

        result = await db_session.execute(query)
        instance: EventOccurrence | None = result.scalars().one_or_none()
        if not instance:
            raise EventOccuranceNotFoundHTTPException

        return instance
