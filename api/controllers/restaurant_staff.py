from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models import restaurant_staff as staff_model  # Import the staff model
from ..schemas import restaurant_staff as staff_schema  # Import the staff schema


def get_all_restaurant_staff(db: Session):
    # Query all staff members from the database
    staff_members = db.query(staff_model.RestaurantStaff).all()
    return staff_members


def create_restaurant_staff(db: Session, request: staff_schema.RestaurantStaffCreate):
    # Check if staff ID already exists to prevent duplicates
    existing_staff = db.query(staff_model.RestaurantStaff).filter(
        staff_model.RestaurantStaff.staff_id == request.staff_id).first()
    if existing_staff:
        raise HTTPException(status_code=400, detail="Staff member with this ID already exists.")

    # Create and add a new staff member to the database
    new_staff = staff_model.RestaurantStaff(
        staff_id=request.staff_id,  # Unique staff ID
        role=request.role,  # Role of the staff member
        name=request.name  # Staff member's name
    )

    db.add(new_staff)
    db.commit()
    db.refresh(new_staff)
    return new_staff  # Return the created staff member


def get_restaurant_staff_by_id(db: Session, staff_id: int):
    # Query the staff member by their unique staff ID
    staff = db.query(staff_model.RestaurantStaff).filter(
        staff_model.RestaurantStaff.staff_id == staff_id).first()

    # Raise a 404 error if the staff member is not found
    if not staff:
        raise HTTPException(status_code=404, detail="Staff member not found.")

    return staff


def update_restaurant_staff(db: Session, staff_id: int, request: staff_schema.RestaurantStaffCreate):
    # Find the staff member to update by their staff ID
    staff_to_update = db.query(staff_model.RestaurantStaff).filter(
        staff_model.RestaurantStaff.staff_id == staff_id).first()

    # Raise a 404 error if staff member does not exist
    if not staff_to_update:
        raise HTTPException(status_code=404, detail="Staff member not found.")

    # Update the staff member's details
    staff_to_update.name = request.name  # Update name
    staff_to_update.role = request.role  # Update role

    db.commit()  # Commit the changes
    db.refresh(staff_to_update)  # Refresh with updated data
    return staff_to_update


def delete_restaurant_staff(db: Session, staff_id: int):
    # Find the staff member to delete by their staff ID
    staff_to_delete = db.query(staff_model.RestaurantStaff).filter(
        staff_model.RestaurantStaff.staff_id == staff_id).first()

    # Raise a 404 error if the staff member does not exist
    if not staff_to_delete:
        raise HTTPException(status_code=404, detail="Staff member not found.")

    # Delete the staff member and commit the change to the database
    db.delete(staff_to_delete)
    db.commit()

    return {"detail": f"Staff member with staff_id {staff_id} deleted successfully."}
