from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..dependencies.database import Base  # Import the base class for the model

class Promotion(Base):
    __tablename__ = 'promotions'

    # Primary key for the promotion record
    id = Column(Integer, primary_key=True, index=True)

    # Indicates if the promotion is valid ('yes' or 'no')
    is_valid = Column(String(3), default='yes')  # Default to 'yes'

    # Foreign key linking the promotion to a specific order
    order_id = Column(Integer, ForeignKey('orders.id'))

    # Foreign key linking the promotion to a specific user
    user_id = Column(Integer, ForeignKey('users.id'))

    # Defines the relationship with the Order model
    # Allows access to the order this promotion is linked to
    order = relationship('Order', back_populates='promotions')

    # Defines the relationship with the User model
    # Allows access to the user who created or applied this promotion
    user = relationship('User', back_populates='promotions')

    # Defines the relationship with the OrderItem model
    # Allows access to the items in the order that this promotion applies to
    order_items = relationship('OrderItem', back_populates='promotion')