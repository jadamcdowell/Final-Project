from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..dependencies.database import Base  # Import the base class for the model

class RestaurantStaff(Base):
    __tablename__ = "restaurant_staff"

    # Unique identifier for each staff member (Primary Key)
    staff_id = Column(Integer, primary_key=True, index=True)

    # Role of the staff member (e.g., Manager, Server, etc.)
    role = Column(String(50), nullable=False)

    # Name of the staff member
    name = Column(String(100), index=True, nullable=False)

    # Defines a one-to-many relationship with the MenuItem model
    # Each staff member can be responsible for multiple menu items
    menu_items = relationship("MenuItem", back_populates="staff", cascade="all, delete-orphan")