from pydantic import BaseModel
from typing import List, Optional


# Base model for order items
class OrderItemBase(BaseModel):
    quantity: int
    menu_item_id: int  # Linking to MenuItem

    class Config:
        orm_mode = True


# Model for creating orders with user and items
class OrderCreate(BaseModel):
    user_id: int  # User making the order
    order_type: str
    status: str = "pending"
    order_items: List[OrderItemBase]  # List of order items
    promo_code: str

    class Config:
        orm_mode = True


# Model for outputting order details
class OrderOut(BaseModel):
    id: int
    user_id: int
    order_type: str
    status: str
    order_items: List[OrderItemBase]  # List of order items
    tracking_number: str

    class Config:
        orm_mode = True


# Internal model for order data (extends OrderOut)
class Order(OrderOut):
    class Config:
        orm_mode = True
        