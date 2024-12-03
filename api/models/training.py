# app/models/training.py

from sqlalchemy import Column, Integer, String, Text, DateTime
from ..dependencies.database import Base
from datetime import datetime

class TrainingModel(Base):
    __tablename__ = "training"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(Text)
    status = Column(String(50), default="open")  # default is 'open', but can be changed
    created_at = Column(DateTime, default=datetime.utcnow)
