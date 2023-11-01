from pydantic import BaseModel
from uuid import UUID
from datetime import date, datetime, timedelta
from enum import Enum

from sqlalchemy import text


from app.routers.api_v1.events.utils import (
    get_previous_sunday,
    get_time_from_datetime,
    last_datetime_of_current_year,
)


# days enum
class Day(Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thurday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"


class Actions(Enum):
    THIS_EVENT = "This event"
    THIS_AND_FOLLOWING_EVENTS = "Following Events"
    ALL_EVENTS = "All events"


class EventBaseSchema(BaseModel):
    event_name: str
    course_number: str | None = None
    description: str | None = None
    location: str | None = None
    event_started_at: date | None


class EventUpdateSchema(BaseModel):
    event_name: str
    course_number: str | None = None
    description: str | None = None
    location: str | None = None


class OccuranceBaseSchema(BaseModel):
    start_time: datetime
    end_time: datetime
    description: str | None = None
    location: str | None = None

    @property
    def get_json(self):
        new_json = {}
        if self.description:
            new_json["description"] = self.description
        if self.location:
            new_json["location"] = self.location
        new_json.update(
            {
                "start_time": text(
                    f"date(start_time) + '{get_time_from_datetime(self.start_time)}'::time"
                ),
                "end_time": text(
                    f"date(end_time) + '{get_time_from_datetime(self.end_time)}'::time"
                ),
            }
        )
        return new_json


class EventCreateSchema(EventBaseSchema):
    start_time: datetime
    end_time: datetime
    repeating_pattern: set[Day]
    repeat_until: datetime = (
        last_datetime_of_current_year()
    )  # default is the last datetime of the year


class OccuranceSchema(OccuranceBaseSchema):
    occurrence_id: UUID

    class Config:
        from_attributes = True


class EventSchema(EventBaseSchema):
    event_id: UUID
    user_id: UUID
    occurance: list[OccuranceSchema]


class EventSchemaCreated(EventBaseSchema):
    event_id: UUID
    user_id: UUID

    class Config:
        from_attributes = True


class DateRangeGetEvent(BaseModel):
    start_date: date = get_previous_sunday()
    end_date: date = get_previous_sunday() + timedelta(days=7)

    def convert_to_datetime(self):
        self.start_date = datetime.combine(self.start_date, datetime.min.time())
        self.end_date = datetime.combine(self.end_date, datetime.min.time())


class EventSchemaReverse(BaseModel):
    event_id: UUID
    event_name: str
    course_number: str | None = None


class OccuranceSchemaReverse(OccuranceBaseSchema):
    occurrence_id: UUID
    event: EventSchemaReverse

    class Config:
        from_attritbutes = True
