from pydantic import BaseModel
from datetime import datetime


# Base model for feedback
class FeedbackBase(BaseModel):
    comments: str
    rating: int


# Model for creating new feedback
class FeedbackCreate(FeedbackBase):
    user_id: int


# Model for output feedback
class FeedbackOut(FeedbackBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True