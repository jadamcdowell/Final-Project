from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from ..dependencies.database import Base # Import the base class for the model


class Feedback(Base):
    __tablename__ = "feedback"  # Table name in the database

    # Primary key for the feedback entry
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Foreign key to link feedback to a specific user (from the 'users' table)
    user_id = Column(Integer, ForeignKey("users.id"))

    # Feedback comments, with a maximum length of 255 characters
    comments = Column(String(255), nullable=False)

    # Rating associated with the feedback
    rating = Column(Integer, nullable=False)

    # Timestamp for when the feedback was created
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to the 'User' model, allowing access to the associated user's data
    user = relationship("User")