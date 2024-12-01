from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..dependencies.database import Base  # Import the base class for the model

class Payment(Base):
    __tablename__ = 'payments'

    # Primary key for the payment record
    id = Column(Integer, primary_key=True, index=True)

    # Foreign key linking the payment to a specific order
    order_id = Column(Integer, ForeignKey('orders.id'))

    # Foreign key linking the payment to a specific user
    user_id = Column(Integer, ForeignKey('users.id'))

    # Payment method (e.g., 'Credit Card', 'PayPal', etc.)
    payment_method = Column(String)

    # Defines the relationship with the User model
    # Allows access to the user who made the payment
    user = relationship('User', back_populates='payments')

    # Defines the relationship with the Order model
    # Allows access to the order associated with this payment
    order = relationship('Order', back_populates='payments')