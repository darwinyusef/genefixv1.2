from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Configuration(BaseModel):
    id: int
    key: str
    value: Optional[str]
    description: Optional[str]
    type: Optional[str]
    state: Optional[str]
    id_user: Optional[int]

    class Config:
        from_attributes = True

class RecoverPassRequest(BaseModel):
    type: str  # "email" o "password"
    email: str
    
    
class ChangeRequest(BaseModel):
    type: str  # "email" o "password"
    change: str