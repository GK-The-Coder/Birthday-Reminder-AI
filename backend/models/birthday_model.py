from datetime import date

from pydantic import BaseModel, EmailStr, Field


class Birthday(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    birthday: date


class WishRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)

class EmailRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr