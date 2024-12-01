from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..models import menu_items as model  # Import MenuItem model
from ..models import restaurant_staff as staff_model  # Import RestaurantStaff model
from ..schemas import menu_items as menu_schema  # Import MenuItem schema


# Fetch all menu items
def read_all(db: Session):
    menu_items = db.query(model.MenuItem).all()
    if not menu_items:
        raise HTTPException(status_code=404, detail="No menu items found.")
    return menu_items


# Fetch a single menu item by ID
def read_one(db: Session, menu_item_id: int):
    menu_item = db.query(model.MenuItem).filter(model.MenuItem.id == menu_item_id).first()
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found.")
    return menu_item


# Create a new menu item (only accessible by managers)
def create_menu_item(db: Session, request: menu_schema.MenuItemCreate):
    staff_id = request.staff_id
    staff = db.query(staff_model.RestaurantStaff).filter(staff_model.RestaurantStaff.staff_id == staff_id).first()

    # Check if staff is a manager
    if not staff or staff.role.lower() != "manager":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Permission denied. Only managers can add menu items.")

    # Create and save new menu item
    new_item = model.MenuItem(
        name=request.name,
        description=request.description,
        price=request.price,
        staff_id=staff_id
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


# Update an existing menu item (only accessible by managers)
def update_menu_item(db: Session, request: menu_schema.MenuItemCreate, menu_item_id: int):
    staff_id = request.staff_id
    staff = db.query(staff_model.RestaurantStaff).filter(staff_model.RestaurantStaff.staff_id == staff_id).first()

    # Check if staff is a manager
    if not staff or staff.role.lower() != "manager":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Permission denied. Only managers can update menu items.")

    # Find and update menu item
    menu_item = db.query(model.MenuItem).filter(model.MenuItem.id == menu_item_id).first()
    if not menu_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found.")

    menu_item.name = request.name
    menu_item.description = request.description
    menu_item.price = request.price
    db.commit()
    db.refresh(menu_item)
    return menu_item


# Delete a menu item (only accessible by managers)
def delete_menu_item(db: Session, menu_item_id: int, staff_id: int):
    staff = db.query(staff_model.RestaurantStaff).filter(staff_model.RestaurantStaff.staff_id == staff_id).first()

    # Check if staff is a manager
    if not staff or staff.role.lower() != "manager":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Permission denied. Only managers can delete menu items.")

    # Find and delete menu item
    menu_item = db.query(model.MenuItem).filter(model.MenuItem.id == menu_item_id).first()
    if not menu_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found.")

    db.delete(menu_item)
    db.commit()
    return {"detail": "Menu item deleted successfully."}
