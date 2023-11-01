from app.exceptions import NotFoundHTTPException


# event_occurance_not_found Exception
EventOccuranceNotFoundHTTPException = NotFoundHTTPException(
    msg="Event Occurance not found"
)
