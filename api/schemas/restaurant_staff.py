from pydantic import BaseModel


# Schema for creating restaurant staff
class RestaurantStaffCreate(BaseModel):
    staff_id: int
    name: str
    role: str

    class Config:
        orm_mode = True


# Schema for outputting restaurant staff details
class RestaurantStaffOut(BaseModel):
    staff_id: int  # Staff identifier
    name: str
    role: str

    class Config:
        orm_mode = True
