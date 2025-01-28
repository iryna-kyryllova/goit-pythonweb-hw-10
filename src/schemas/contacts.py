from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, EmailStr, field_validator


class ContactBase(BaseModel):
    first_name: str = Field(max_length=50, min_length=2)
    last_name: str = Field(max_length=50, min_length=2)
    email: EmailStr
    phone_number: str = Field(max_length=20, min_length=6)
    birthday: date
    additional_data: Optional[str] = Field(max_length=200)

    @field_validator("birthday")
    def validate_birthday(cls, value):
        if value > date.today():
            raise ValueError("Birthday cannot be in the future")
        return value


class ContactResponse(ContactBase):
    id: int
    created_at: datetime | None
    updated_at: Optional[datetime] | None
    model_config = ConfigDict(from_attributes=True)


class ContactBirthdayRequest(BaseModel):
    days: int = Field(ge=0, le=365)
