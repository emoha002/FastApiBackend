import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db
from app.routers.api_v1.auth.dependencies import get_current_user
from app.routers.api_v1.auth.models import User
from app.routers.api_v1.events.models import CalendarEvent, EventOccurrence

from app.routers.api_v1.events.schemas import (
    DateRangeGetEvent,
    EventCreateSchema,
    OccuranceSchemaReverse,
)
from app.routers.api_v1.events.service import create_new_event, get_all_events_by_range

event_router = APIRouter(
    prefix="/event",
    tags=["Event"],
    responses={404: {"description": "Incorrect Not found"}},
)


@event_router.post(
    "/add_event",
    status_code=201,
    response_model=dict[str, str],
)
async def add_events(
    event_create: EventCreateSchema,
    user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db),
):
    db_event: CalendarEvent = await create_new_event(
        db_session=db_session, create_event=event_create, user=user
    )
    return {"status": "success", "message": "Event created successfully"}


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


# delete event -> deletes all event and it's children
# delete after specific date
# delete only one specific
# update only one
# get only one
# add only one event occurance that is going to happen at a time
