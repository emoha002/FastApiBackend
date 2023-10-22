from typing import Annotated, Any

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession


from jose import jwt
from app.database.database import get_db
from app.routers.api_v1.auth.constants import SECRET_KEY
from app.routers.api_v1.auth.exceptions import INVALID_CREDENTIAL, TOKEN_EXPIRED
from app.routers.api_v1.auth.models import User
from app.routers.api_v1.auth.service import has_time_passed

oauth2_schema = OAuth2PasswordBearer(tokenUrl="./api_v1/auth/sign_in")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_schema)],
    db_session: AsyncSession = Depends(get_db),
) -> User:
    try:
        payload: dict[str, Any] = jwt.decode(token, SECRET_KEY)
        if has_time_passed(payload["exp"]):
            raise TOKEN_EXPIRED

        user: User | None = await User.find_by_username(db_session, payload["username"])
        if not user:
            raise INVALID_CREDENTIAL
        return user
    except Exception as e:
        await db_session.rollback()
        raise e


async def get_current_active_user(
    user: Annotated[User, Depends(get_current_user)],
) -> User:
    if not user.is_activated:
        raise INVALID_CREDENTIAL
    return user
