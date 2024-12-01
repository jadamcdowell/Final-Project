from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..dependencies.database import Base  # Import the base class for the model


# Order model representing customer orders
class Order(Base):
    __tablename__ = 'orders' # Table name in the database

    # Primary key for the order
    id = Column(Integer, primary_key=True, index=True)

    # Foreign key linking the order to a specific user (from 'users' table)
    user_id = Column(Integer, ForeignKey('users.id'))

    # Relationship to the User model, representing the user who placed the order
    user = relationship('User', back_populates='orders')

    # Relationship to the OrderItem model, representing items included in the order
    order_items = relationship('OrderItem', back_populates='order')

    # Defines the relationship with the Payment model
    payments = relationship('Payment', back_populates='order',
                            cascade='all, delete-orphan')

    # Defines the relationship with the Promotion model
    promotions = relationship('Promotion', back_populates='order',
                              cascade="all, delete-orphan")


# OrderItem model representing individual items within an order
class OrderItem(Base):
    __tablename__ = 'order_items'

    # Primary key for the order item
    id = Column(Integer, primary_key=True, index=True)

    # Quantity of the specific item in the order (defaults to 1 if not provided)
    quantity = Column(Integer, nullable=False, default=1)

    # Foreign key linking the order item to a specific menu item (from 'menu_items' table)
    menu_item_id = Column(Integer, ForeignKey('menu_items.id'))

    # Foreign key linking the order item to a specific order (from 'orders' table)
    order_id = Column(Integer, ForeignKey('orders.id'))

    # Foreign key linking the order item to a specific promotion (from 'promotions' table, if any)
    promotion_id = Column(Integer, ForeignKey('promotions.id'))

    # Relationship to the MenuItem model, representing the specific item in the menu
    menu_item = relationship('MenuItem', back_populates='order_items')

    # Relationship to the Order model, representing the order this item is part of
    order = relationship('Order', back_populates='order_items')

    # Relationship to the Promotion model, representing the promotion applied to this order item (if any)
    promotion = relationship('Promotion', back_populates='order_items')