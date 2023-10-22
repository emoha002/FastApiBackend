# imoprt pydantic email validator

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    username: str
    fullname: str


class UserCreate(UserBase):
    password: str


class UserSchema(UserBase):
    id: UUID
    created_at: datetime
    is_activated: bool
    is_admin: bool

    class Config:
        from_attributes = True
