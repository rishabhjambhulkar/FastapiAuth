from pydantic import BaseModel, EmailStr
from typing import Union
from datetime import datetime

class BaseResponse(BaseModel):
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    registered_at: Union[None, datetime] = None