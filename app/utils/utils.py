from typing import Annotated

from fastapi import Header

from app.exceptions import NotFoundHTTPException


# add utils here


# example access token
async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise NotFoundHTTPException()


days = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}


def get_day_index(day: str) -> int:
    return days[day.lower()]
