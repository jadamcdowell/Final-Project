from pydantic import BaseModel


# Base schema for promotions
class PromotionBase(BaseModel):
    is_valid: str
    order_id: int
    user_id: int

    class Config:
        orm_mode = True


# Schema for creating promotions
class PromotionCreate(PromotionBase):
    pass


# Schema for outputting promotion details
class PromotionOut(PromotionBase):
    id: int  # Promotion ID

    class Config:
        orm_mode = True
        