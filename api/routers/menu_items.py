from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..controllers import menu_items as controller  # Import the menu items controller
from ..schemas import menu_items as schema  # Import the menu items schema
from ..dependencies.database import get_db  # Import the database dependency

# Create a new APIRouter instance for the "Menu Items" route
router = APIRouter(
    tags=['Menu Items'],
    prefix="/menuitems"
)


# Endpoint to get all menu items
@router.get("/", response_model=list[schema.MenuItemOut])
def read_all_menu_items(db: Session = Depends(get_db)):
    # Calls the controller to fetch all menu items from the database
    return controller.read_all(db)


# Endpoint to create a new menu item (Only Managers can create menu items)
@router.post("/", response_model=schema.MenuItemOut)
def create_menu_item(request: schema.MenuItemCreate, db: Session = Depends(get_db)):
    # Calls the controller to create a new menu item
    return controller.create_menu_item(db=db, request=request)


# Endpoint to get a specific menu item by ID
@router.get("/{menu_item_id}", response_model=schema.MenuItemOut)
def read_one_menu_item(menu_item_id: int, db: Session = Depends(get_db)):
    # Calls the controller to fetch a specific menu item by ID
    return controller.read_one(db, menu_item_id=menu_item_id)


# Endpoint to update an existing menu item (Only Managers can update menu items)
@router.put("/{menu_item_id}", response_model=schema.MenuItemOut)
def update_menu_item(menu_item_id: int, request: schema.MenuItemCreate, db: Session = Depends(get_db)):
    # Calls the controller to update an existing menu item
    return controller.update_menu_item(db=db, request=request, menu_item_id=menu_item_id)


# Endpoint to delete a menu item (Only Managers can delete menu items)
@router.delete("/{menu_item_id}")
def delete_menu_item(menu_item_id: int, staff_id: int, db: Session = Depends(get_db)):
    # Calls the controller to delete a menu item by ID
    return controller.delete_menu_item(db=db, menu_item_id=menu_item_id, staff_id=staff_id)