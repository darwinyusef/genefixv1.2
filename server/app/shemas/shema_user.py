# Pydantic schemas
from typing import Optional
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]


class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]


class UserOut(BaseModel):
    id: int
    username: str
    name: Optional[str]
    email: Optional[str]

    class Config:
        from_attributes = True

class UserRolActive(BaseModel):
    username: str
    name: Optional[str]
    rol: Optional[str]