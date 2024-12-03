# app/schemas/training.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

class TrainingBase(BaseModel):
    title: str = Field(..., example="Training on Customer Support Process", description="Enter the title of the training session")
    description: str = Field(..., example="Training to improve customer support skills", description="Provide a detailed description of the training session")
    
    status: Literal["open", "in progress", "running", "completed", "closed"] = "open"  # Default value is 'open'
    # status options: open - ticket is open, in progress - being worked on, running - actively running, completed - finished, closed - closed

class TrainingCreate(TrainingBase):
    pass

class TrainingOut(TrainingBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
