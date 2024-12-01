from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..dependencies.database import Base  # Import the base class for the model


# MenuItem model representing items on the restaurant menu
class MenuItem(Base):
    __tablename__ = "menu_items"  # Table name in the database

    # Primary key for the menu item
    id = Column(Integer, primary_key=True, index=True)

    # Name of the menu item, indexed for faster lookups
    name = Column(String, index=True)

    # Description of the menu item (e.g., ingredients or preparation style)
    description = Column(String)

    # Price of the menu item
    price = Column(Float)

    # Foreign key to link the menu item to a specific staff member (from 'restaurant_staff' table)
    staff_id = Column(Integer, ForeignKey("restaurant_staff.staff_id"))

    # Relationship to the 'RestaurantStaff' model, representing the staff member responsible for the menu item
    staff = relationship("RestaurantStaff", back_populates="menu_items")

    # Relationship to the 'OrderItem' model, representing the items in customer orders
    order_items = relationship('OrderItem', back_populates='menu_item')  # Links to OrderItem (menu item in an order)
