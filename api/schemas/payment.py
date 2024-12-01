from pydantic import BaseModel


# Base schema for payments
class PaymentBase(BaseModel):
    order_id: int
    payment_method: str
    user_id: int

    class Config:
        orm_mode = True


# Schema for creating payments
class PaymentCreate(PaymentBase):
    pass  # Inherits from PaymentBase


# Schema for outputting payment details
class PaymentOut(PaymentBase):
    id: int

    class Config:
        orm_mode = True