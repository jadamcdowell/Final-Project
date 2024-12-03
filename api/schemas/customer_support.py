from pydantic import BaseModel
from datetime import datetime

# Base schema for customer support data
class CustomerSupportBase(BaseModel):
    title: str
    description: str
    status: str

# Schema for creating a customer support ticket
class CustomerSupportCreate(CustomerSupportBase):
    # Add any additional fields for creation if necessary
    pass

# Schema for outputting customer support ticket details
class CustomerSupportOut(CustomerSupportBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
