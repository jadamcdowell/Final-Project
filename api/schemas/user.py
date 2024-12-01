from pydantic import BaseModel
from datetime import datetime

# Base schema for user data
class UserBase(BaseModel):
    username: str
    name: str
    email: str

# Schema for creating a user
class UserCreate(UserBase):
    password: str

# Schema for outputting user details
class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True