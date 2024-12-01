from pydantic import BaseModel


# Model for creating/updating menu items
class MenuItemCreate(BaseModel):
    name: str
    description: str
    price: float
    staff_id: int  # Staff creating/updating the item

    class Config:
        orm_mode = True


# Model for outputting menu item data
class MenuItemOut(MenuItemCreate):
    id: int  # Includes generated menu item ID
    