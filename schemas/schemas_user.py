# Schematics of the Users endpoint.

from pydantic import BaseModel, EmailStr
from typing import Optional

class user_create(BaseModel):
    email_id: EmailStr
    password: str

class user_display(BaseModel):
    id: int
    email_id: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
