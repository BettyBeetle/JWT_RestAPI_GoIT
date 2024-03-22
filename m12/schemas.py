from datetime import date, datetime
from pydantic import BaseModel, Field
from typing import Optional

class ContactsIn(BaseModel):
    first_name: str = Field(min_length=4, max_length=16)
    last_name: str = Field(min_length=4, max_length=16)
    email: str
    phone_number: str
    date_of_birth: date
    nick: Optional[str]= None
    password: str = Field(min_length=6, max_length=10)

class ContactsOut(ContactsIn):
    id: int
    password: Optional[str] = None

    class Config:
        orm_mode = True



class UserIn(BaseModel):
    username: str = Field(min_length=4, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)

class UserOut(UserIn):
    id: int
    username: str
    email: str
    created_at: datetime


    class Config:
        orm_mode = True

class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"