from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import user as controller  # Import the user controller functions
from ..schemas import user as schema  # Import the user schema
from ..dependencies.database import get_db  # Import database dependency to get the DB session

# Create an APIRouter instance for the "User" route
router = APIRouter(
    tags=['User'],
    prefix="/users"
)


# Endpoint to create a new user
@router.post("/", response_model=schema.UserOut)
def create_user(request: schema.UserCreate, db: Session = Depends(get_db)):
    # Create a new user and store it in the database
    return controller.create_user(db=db, request=request)


# Endpoint to get all users
@router.get("/", response_model=list[schema.UserOut])
def read_all_users(db: Session = Depends(get_db)):
    # Fetch all users from the database
    return controller.read_all(db)


# Endpoint to get a specific user by their ID
@router.get("/{user_id}", response_model=schema.UserOut)
def read_one_user(user_id: int, db: Session = Depends(get_db)):
    # Fetch a specific user by their ID from the database
    return controller.read_one(db, user_id=user_id)


# Endpoint to update a specific user by their ID
@router.put("/{user_id}", response_model=schema.UserOut)
def update_user(user_id: int, request: schema.UserCreate, db: Session = Depends(get_db)):
    # Update an existing user's information by their user_id
    return controller.update(db=db, request=request, user_id=user_id)


# Endpoint to delete a user by their ID
@router.delete("/{user_id}")
def delete(user_id: int, db: Session = Depends(get_db)):
    # Delete a user from the database by their user_id
    return controller.delete(db=db, user_id=user_id)