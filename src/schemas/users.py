from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, EmailStr, field_validator


# Схема користувача
class User(BaseModel):
    id: int
    username: str
    email: str
    avatar: str

    model_config = ConfigDict(from_attributes=True)


# Схема для запиту реєстрації
class UserCreate(BaseModel):
    username: str
    email: str
    password: str


# Схема для токену
class Token(BaseModel):
    access_token: str
    token_type: str


class RequestEmail(BaseModel):
    email: EmailStr

