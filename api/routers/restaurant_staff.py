from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import restaurant_staff as controller  # Import the restaurant staff controller functions
from ..schemas import restaurant_staff as staff_schema  # Import the restaurant staff schema
from ..dependencies.database import get_db  # Import the database dependency to get DB session

# Create an APIRouter instance for the "Restaurant Staff" route
router = APIRouter(
    tags=["Restaurant Staff"],
    prefix="/restaurant_staff"
)


# Endpoint to get all restaurant staff members
@router.get("/", response_model=list[staff_schema.RestaurantStaffOut])
def read_all_restaurant_staff(db: Session = Depends(get_db)):
    # Fetch all restaurant staff members from the database
    return controller.get_all_restaurant_staff(db=db)


# Route to create a new restaurant staff member
@router.post("/create", response_model=staff_schema.RestaurantStaffOut)
def create_restaurant_staff(request: staff_schema.RestaurantStaffCreate, db: Session = Depends(get_db)):
    # Create a new staff member and store it in the database
    return controller.create_restaurant_staff(db=db, request=request)


# Endpoint to get a specific staff member by their ID
@router.get("/{staff_id}", response_model=staff_schema.RestaurantStaffOut)
def read_restaurant_staff(staff_id: int, db: Session = Depends(get_db)):
    # Fetch a specific staff member using the provided staff_id
    return controller.get_restaurant_staff_by_id(db=db, staff_id=staff_id)


# Endpoint to update a specific staff member by their ID
@router.put("/{staff_id}", response_model=staff_schema.RestaurantStaffOut)
def update_restaurant_staff(staff_id: int, request: staff_schema.RestaurantStaffCreate, db: Session = Depends(get_db)):
    # Update an existing staff member's information by their staff_id
    return controller.update_restaurant_staff(db=db, staff_id=staff_id, request=request)


# Simple delete for a restaurant staff member by their ID
@router.delete("/{staff_id}", response_model=dict)
def delete_restaurant_staff(staff_id: int, db: Session = Depends(get_db)):
    # Delete a staff member by their staff_id and return a success message
    return controller.delete_restaurant_staff(db=db, staff_id=staff_id)