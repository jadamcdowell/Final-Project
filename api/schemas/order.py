from pydantic import BaseModel
from typing import List


# Base model for order items
class OrderItemBase(BaseModel):
    quantity: int
    menu_item_id: int  # Linking to MenuItem

    class Config:
        orm_mode = True


# Model for creating orders with user and items
class OrderCreate(BaseModel):
    user_id: int  # User making the order
    order_items: List[OrderItemBase]  # List of order items

    class Config:
        orm_mode = True


# Model for outputting order details
class OrderOut(BaseModel):
    id: int
    user_id: int
    order_items: List[OrderItemBase]  # List of order items

    class Config:
        orm_mode = True


# Internal model for order data (extends OrderOut)
class Order(OrderOut):
    class Config:
        orm_mode = True
        