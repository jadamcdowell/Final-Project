from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Base schema for user data (doesn't require username or password for guest users)
class UserBase(BaseModel):
    username: Optional[str]  # Username is optional
    name: str
    email: str  # Required
    phone_number: str  # Required 

# Schema for creating a user (only required for registered users)
class UserCreate(UserBase):
    password: str  # Password is required only for registered users

# Schema for outputting user details
class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True