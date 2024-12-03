from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional
from ..dependencies.database import Base  # Import the base class for the model


class Promotion(Base):
    __tablename__ = 'promotions'

    # Primary key for the promotion record
    id = Column(Integer, primary_key=True, index=True)

    # Unique code for the promotion
    code = Column(String(50), unique=True, nullable=False)

    # Optional description for the promotion
    description = Column(String(255), nullable=True)

    # Discount percentage for the promotion
    discount_percentage = Column(Float, nullable=False)

    # Start date for the promotion
    start_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Expiration date for the promotion
    expiration_date = Column(DateTime, nullable=False)

    # Whether the promotion is currently valid
    is_valid = Column(Boolean, default=True, nullable=False)

    # Foreign key linking the promotion to a specific Manager (staff member)
    staff_id = Column(Integer, ForeignKey('restaurant_staff.staff_id'), nullable=False)

    # Relationships
    staff = relationship('RestaurantStaff', back_populates='promotions')

    # Defines the relationship with the OrderItem model
    # Allows access to the items in the order that this promotion applies to
    order_items = relationship('OrderItem', back_populates='promotion')