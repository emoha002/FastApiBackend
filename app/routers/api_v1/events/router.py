from datetime import datetime
import uuid
from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db
from app.routers.api_v1.auth.dependencies import get_current_user
from app.routers.api_v1.auth.models import User
from app.routers.api_v1.events.models import CalendarEvent, EventOccurrence

from app.routers.api_v1.events.schemas import (
    Actions,
    DateRangeGetEvent,
    EventCreateSchema,
    EventSchemaCreated,
    EventUpdateSchema,
    OccuranceBaseSchema,
    OccuranceSchemaReverse,
)
from app.routers.api_v1.events.service import (
    create_new_event,
    delete_reccurent_event,
    get_all_events_by_range,
    update_reccurent_event,
)

event_router = APIRouter(
    prefix="/event",
    tags=["Event"],
    responses={404: {"description": "Incorrect Not found"}},
)


@event_router.post("/add_event", status_code=201, response_model=EventSchemaCreated)
async def add_events(
    event_create: EventCreateSchema,
    user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db),
):
    if event_create.event_started_at is None:
        event_create.event_started_at = datetime.utcnow().date()
    db_event: CalendarEvent = await create_new_event(
        db_session=db_session, create_event=event_create, user=user
    )
    return db_event


@event_router.post(
    "/get_events",
    status_code=200,
    response_model=list[OccuranceSchemaReverse],
)
async def get_events(
    date_range: DateRangeGetEvent,
    user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db),
):
    res = await get_all_events_by_range(
        db_session=db_session, user=user, date_range=date_range
    )
    return res


@event_router.post(
    "/get_one/event/{event_occurance_id}",
    response_model=OccuranceSchemaReverse,
)
async def get_one_event(
    event_occurance_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db),
):
    return await EventOccurrence.get_by_occurance_id(
        db_session,
        event_occurance_id,
        user,
    )


# delete calendar event
@event_router.delete(
    "/delete/event/{event_id}",
    response_model=dict[str, str],
)
async def delete_event(
    event_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db),
):
    await CalendarEvent.delete_event_by_event_id(
        db_session,
        event_id,
        user,
    )
    # await event.delete(db_session)
    return {"status": "success", "message": "Event deleted successfully"}


# update calendar event
@event_router.put(
    "/update/event/{event_id}",
    response_model=EventSchemaCreated,
)
async def update_event(
    event_data: EventUpdateSchema,
    event_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db),
):
    db_calendar_event: CalendarEvent = await CalendarEvent.get_event_by_event_id(
        db_session,
        event_id,
        user,
    )
    await db_calendar_event.update(db=db_session, **event_data.model_dump())
    return db_calendar_event


# update occuring event
@event_router.put(
    "/update/occurance/{event_occurance_id}",
)
async def update_occurance(
    event_occurance_id: uuid.UUID,
    action: Actions = Body(),
    occurance_data: OccuranceBaseSchema = Body(),
    user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db),
):
    await update_reccurent_event(
        db_session=db_session,
        action=action,
        occurance_data=occurance_data,
        occurrence_id=event_occurance_id,
        user=user,
    )
    return {"success": True, "message": "Event updated successfully"}


@event_router.delete(
    "/delete/occurance/{event_occurance_id}",
    response_model=dict[str, str],
)
async def delete_occurance(
    event_occurance_id: uuid.UUID,
    action: Actions = Body(embed=True),
    user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db),
):
    await delete_reccurent_event(
        db_session=db_session,
        occurrence_id=event_occurance_id,
        user=user,
        action=action,
    )
    return {"status": "success", "message": "Event deleted successfully"}
