from app.exceptions import (
    AuthFailedHTTPException,
    AuthTokenExpiredHTTPException,
    BadRequestHTTPException,
    NotFoundHTTPException,
)

USER_NAME_IS_TAKEN = BadRequestHTTPException(msg="Username is already taken")
USER_NOT_ACTIVATED: BadRequestHTTPException = BadRequestHTTPException(
    msg="User is not activated"
)

USER_NOT_FOUND = NotFoundHTTPException("User Not Found")

USER_ALREADY_ACTIVATED = BadRequestHTTPException(msg="user is already activated")

EMAIL_PHONE_HAS_BEEN_REGISTERED = BadRequestHTTPException(
    msg="email address or phone number is already registered"
)
# already registered exception

ALREADY_REGISTERED = BadRequestHTTPException(msg="Already registered")

UN_AUTHORIZED_ACCESS = AuthFailedHTTPException("Not Authenticated")

UN_AUTHORIZED_ACCESS_ADMIN = AuthFailedHTTPException("Not admin")

GOOGLE_AUTH_FAILED = BadRequestHTTPException(msg="Google Auth Failed")

INVALID_CREDENTIAL = BadRequestHTTPException("Could not validate Credentials")
INCORRECT_PASSWORD = BadRequestHTTPException(msg="Incorrect password")

TOKEN_EXPIRED = AuthTokenExpiredHTTPException()

OTP_EXPIRED = BadRequestHTTPException(msg="OTP has expired")

OTP_NOT_FOUND = NotFoundHTTPException(msg="OTP not found")

OTP_VALIDATION_FAILED = BadRequestHTTPException(msg="OTP validation failed")
