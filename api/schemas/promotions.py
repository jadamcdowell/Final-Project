from pydantic import BaseModel
from datetime import datetime

# Model for creating/updating promotions
class PromotionCreate(BaseModel):
    code: str
    description: str
    discount_percentage: float
    start_date: datetime
    expiration_date: datetime
    is_valid: bool

    class Config:
        orm_mode = True


# Model for outputting promotion data
class PromotionOut(PromotionCreate):
    id: int  # Includes generated promotion ID