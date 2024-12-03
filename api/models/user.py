from fastapi.openapi.models import Schema
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base  # Import the base class for the model

class User(Base):
    __tablename__ = "users"

    # Unique identifier for each user (Primary Key)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Name of the user, indexed for faster querying
    name = Column(String(100), index=True, nullable=False)

    # Email address of the user, unique and indexed for faster querying
    email = Column(String(100), unique=True, index=True, nullable=False)

    # Username of the user, this is optional for guest users
    username = Column(String(255), nullable=True)

    # Phone number of the user, indexed for faster querying (can be required for guest users)
    phone_number = Column(String(100), index=True, nullable=False)

    # Timestamp of when the user was created, default is current time
    created_at = Column(DateTime, default=datetime.utcnow)

    # Password of the user, stored as a string (hashed before storage in real scenarios)
    password = Column(String(255), nullable=True) # Password can be null for guest users

    # One-to-many relationship with the Order model
    # Each user can have multiple orders
    orders = relationship("Order", back_populates="user")

    # One-to-many relationship with the Payment model
    # Each user can have multiple payments
    payments = relationship('Payment', back_populates='user', cascade='all, delete-orphan')