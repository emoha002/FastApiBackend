from datetime import datetime, timedelta
import uuid
from sqlalchemy import and_, delete, update
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.routers.api_v1.auth.models import User
from app.routers.api_v1.events.exceptions import EventOccuranceNotFoundHTTPException
from app.routers.api_v1.events.models import CalendarEvent, EventOccurrence

from app.routers.api_v1.events.schemas import (
    Actions,
    DateRangeGetEvent,
    EventCreateSchema,
    OccuranceBaseSchema,
)
from app.utils.utils import get_day_index


async def create_new_event(
    db_session: AsyncSession,
    create_event: EventCreateSchema,
    user: User,
) -> CalendarEvent:
    db_event: CalendarEvent = CalendarEvent(
        user_id=user.id,
        event_name=create_event.event_name,
        course_number=create_event.course_number,
        repeat_until=create_event.repeat_until,
        event_started_at=create_event.event_started_at,
        description=create_event.description,
    )

    current_date: datetime = datetime.combine(
        create_event.event_started_at, datetime.min.time()
    )
    # add time 0:00:00 to current_date
    # repeating days
    reapeating_day: list[int] = [0] * 7
    for day in create_event.repeating_pattern:
        reapeating_day[get_day_index(day.value)] = 1

    # add the event occurance for the starting date
    db_event_occurances: list[EventOccurrence] = [
        EventOccurrence(
            event_id=db_event.event_id,
            start_time=current_date.replace(
                hour=create_event.start_time.hour,
                minute=create_event.start_time.minute,
            ),
            end_time=current_date.replace(
                hour=create_event.end_time.hour,
                minute=create_event.end_time.minute,
            ),
            location=create_event.location,
        )
    ]
    current_date = current_date + timedelta(days=1)

    # FIXME impplemnent smart jumping mechanism
    while (
        len(create_event.repeating_pattern) and current_date < create_event.repeat_until
    ):
        if reapeating_day[current_date.weekday()]:
            db_event_occurances.append(
                EventOccurrence(
                    event_id=db_event.event_id,
                    start_time=current_date.replace(
                        hour=create_event.start_time.hour,
                        minute=create_event.start_time.minute,
                    ),
                    end_time=current_date.replace(
                        hour=create_event.end_time.hour,
                        minute=create_event.end_time.minute,
                    ),
                    location=create_event.location,
                )
            )

        current_date = current_date + timedelta(days=1)

    try:
        db_event.event_occurrences = db_event_occurances
        await db_event.save(db_session)
    except SQLAlchemyError:
        raise HTTPException(status_code=422, detail="Could not create event")
    return db_event


async def get_all_events_by_range(
    db_session: AsyncSession,
    user: User,
    date_range: DateRangeGetEvent,
):
    query = (
        select(EventOccurrence)
        .join(CalendarEvent, CalendarEvent.event_id == EventOccurrence.event_id)
        .where(
            and_(
                CalendarEvent.user_id == user.id,
                EventOccurrence.start_time >= date_range.start_date,
                EventOccurrence.end_time <= date_range.end_date,
            )
        )
        .options(selectinload(EventOccurrence.event))
    )

    result = await db_session.execute(query)
    db_calendar_events: list[EventOccurrence] = list(result.scalars().all())
    return db_calendar_events


async def update_reccurent_event(
    db_session: AsyncSession,
    action: Actions,
    occurance_data: OccuranceBaseSchema,
    occurrence_id: uuid.UUID,
    user: User,
):
    # FIXME add validation to the timespamp
    subquery = (
        select(EventOccurrence.occurrence_id)
        .join(CalendarEvent, CalendarEvent.event_id == EventOccurrence.event_id)
        .where(
            CalendarEvent.user_id == user.id,
        )
    )

    if action == Actions.THIS_EVENT:
        subquery = subquery.where(
            and_(
                EventOccurrence.occurrence_id == occurrence_id,
                CalendarEvent.user_id == user.id,
            )
        )

    query = update(EventOccurrence)

    # If this and future is the one that is selected
    if action == Actions.THIS_AND_FOLLOWING_EVENTS:
        query = query.where(
            EventOccurrence.start_time
            >= (
                select(EventOccurrence.start_time).where(
                    EventOccurrence.occurrence_id == occurrence_id
                )
            )
        )

    if action == Actions.ALL_EVENTS:
        query = query.where(
            EventOccurrence.event_id
            == (
                select(EventOccurrence.event_id).where(
                    EventOccurrence.occurrence_id == occurrence_id
                )
            )
        )

    query = query.where(EventOccurrence.occurrence_id.in_(subquery)).values(
        occurance_data.get_json
    )

    affected_rows = await db_session.execute(query)
    await db_session.commit()
    if affected_rows.rowcount == 0:
        raise EventOccuranceNotFoundHTTPException


async def delete_reccurent_event(
    db_session: AsyncSession, occurrence_id: uuid.UUID, user: User, action: Actions
):
    subquery = (
        select(EventOccurrence.occurrence_id)
        .join(CalendarEvent, CalendarEvent.event_id == EventOccurrence.event_id)
        .where(CalendarEvent.user_id == user.id)
    )

    if action == Actions.THIS_EVENT:
        subquery = subquery.where(
            and_(
                EventOccurrence.occurrence_id == occurrence_id,
            )
        )

    query = delete(EventOccurrence)

    if action == Actions.THIS_AND_FOLLOWING_EVENTS:
        query = query.where(
            EventOccurrence.start_time
            >= (
                select(EventOccurrence.start_time).where(
                    EventOccurrence.occurrence_id == occurrence_id
                )
            )
        )

    if action == Actions.ALL_EVENTS:
        query = query.where(
            EventOccurrence.event_id
            == (
                select(EventOccurrence.event_id).where(
                    EventOccurrence.occurrence_id == occurrence_id
                )
            )
        )

    query = query.where(EventOccurrence.occurrence_id.in_(subquery))

    affected_rows = await db_session.execute(query)
    await db_session.commit()

    if affected_rows.rowcount == 0:
        raise EventOccuranceNotFoundHTTPException
