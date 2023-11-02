from app.exceptions import NotFoundHTTPException, UnprocessableEntityHTTPException


TASK_NOT_FOUND = NotFoundHTTPException(
    msg="Task not found",
)


NOTHING_TO_UPDATE = UnprocessableEntityHTTPException(
    msg="Nothing to update",
)
