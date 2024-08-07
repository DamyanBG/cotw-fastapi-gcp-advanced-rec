from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="First name of the user",
        example="John",
    )
    last_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Last name of the user",
        example="Doe",
    )
    email: EmailStr = Field(
        ..., description="Email of the user", example="john_doe@example.com"
    )
    password: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserId(BaseModel):
    id: str


class User(UserBase, UserId):
    pass


class UserUpdate(UserBase):
    pass
