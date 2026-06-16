from pydantic import BaseModel, EmailStr


class Birthday(BaseModel):
    name: str
    email: EmailStr
    birthday: str


class WishRequest(BaseModel):
    name: str

class EmailRequest(BaseModel):
    name: str
    email: str